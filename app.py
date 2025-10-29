"""
SMS Spam Classifier - Web Application

A Streamlit-based web interface for real-time SMS spam classification.
Uses a pre-trained TF-IDF + Multinomial Naive Bayes model.

Usage:
    streamlit run app.py

Requirements:
    - spam_model.joblib (trained model file)
    - Run 'python train.py' first if model doesn't exist
"""

import streamlit as st
import joblib
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Page configuration
st.set_page_config(
    page_title="SMS Spam Classifier",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)


@st.cache_resource
def load_model(model_path='spam_model.joblib'):
    """
    Load the pre-trained spam classifier model.
    Uses Streamlit's cache to avoid reloading on every interaction.
    
    Args:
        model_path (str): Path to the saved model file
        
    Returns:
        model: Loaded scikit-learn pipeline
        
    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found")
    
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")


@st.cache_data
def load_dataset(file_path='sms_spam_no_header.csv'):
    """
    Load the SMS dataset for visualization.
    Uses Streamlit's cache to avoid reloading on every interaction.
    
    Args:
        file_path (str): Path to the CSV dataset
        
    Returns:
        pandas.DataFrame: Dataset with 'label' and 'text' columns
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_csv(file_path, header=None, names=['label', 'text'])
        return df
    except Exception as e:
        return None


def display_dataset_overview(df):
    """
    Display overview of the dataset with statistics and visualizations.
    
    Args:
        df (pandas.DataFrame): Dataset to visualize
    """
    st.markdown("---")
    st.header("📊 Dataset Overview")
    
    # Calculate statistics
    total_messages = len(df)
    spam_count = len(df[df['label'] == 'spam'])
    ham_count = len(df[df['label'] == 'ham'])
    spam_percentage = (spam_count / total_messages) * 100
    ham_percentage = (ham_count / total_messages) * 100
    
    # Display key metrics
    st.markdown("### 📈 Dataset Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Messages",
            value=f"{total_messages:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Spam Messages",
            value=f"{spam_count:,}",
            delta=f"{spam_percentage:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Ham Messages",
            value=f"{ham_count:,}",
            delta=f"{ham_percentage:.1f}%"
        )
    
    # Create visualizations
    st.markdown("### 📊 Data Distribution")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Ham (Legitimate)', 'Spam (Junk)'],
            values=[ham_count, spam_count],
            hole=0.4,
            marker=dict(colors=['#4caf50', '#f44336']),
            textinfo='label+percent',
            textfont=dict(size=14)
        )])
        
        fig_pie.update_layout(
            title=dict(
                text="Message Type Distribution",
                font=dict(size=16, color='#333')
            ),
            height=350,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = go.Figure(data=[
            go.Bar(
                x=['Ham', 'Spam'],
                y=[ham_count, spam_count],
                marker=dict(color=['#4caf50', '#f44336']),
                text=[f'{ham_count:,}', f'{spam_count:,}'],
                textposition='auto',
                textfont=dict(size=14, color='white')
            )
        ])
        
        fig_bar.update_layout(
            title=dict(
                text="Message Count by Type",
                font=dict(size=16, color='#333')
            ),
            xaxis_title="Message Type",
            yaxis_title="Count",
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Message length analysis
    st.markdown("### 📏 Message Length Analysis")
    
    # Calculate message lengths
    df['message_length'] = df['text'].str.len()
    
    # Create box plot for message lengths
    fig_box = go.Figure()
    
    fig_box.add_trace(go.Box(
        y=df[df['label'] == 'ham']['message_length'],
        name='Ham',
        marker=dict(color='#4caf50'),
        boxmean='sd'
    ))
    
    fig_box.add_trace(go.Box(
        y=df[df['label'] == 'spam']['message_length'],
        name='Spam',
        marker=dict(color='#f44336'),
        boxmean='sd'
    ))
    
    fig_box.update_layout(
        title=dict(
            text="Message Length Distribution (Characters)",
            font=dict(size=16, color='#333')
        ),
        yaxis_title="Message Length (characters)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Display summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Ham Message Statistics:**")
        ham_stats = df[df['label'] == 'ham']['message_length'].describe()
        st.write(f"- Average length: {ham_stats['mean']:.0f} characters")
        st.write(f"- Median length: {ham_stats['50%']:.0f} characters")
        st.write(f"- Max length: {ham_stats['max']:.0f} characters")
    
    with col2:
        st.markdown("**Spam Message Statistics:**")
        spam_stats = df[df['label'] == 'spam']['message_length'].describe()
        st.write(f"- Average length: {spam_stats['mean']:.0f} characters")
        st.write(f"- Median length: {spam_stats['50%']:.0f} characters")
        st.write(f"- Max length: {spam_stats['max']:.0f} characters")


def predict_message(model, message):
    """
    Predict whether a message is spam or ham.
    
    Args:
        model: Trained classifier pipeline
        message (str): SMS message text to classify
        
    Returns:
        tuple: (prediction, confidence_spam, confidence_ham)
            - prediction (str): 'spam' or 'ham'
            - confidence_spam (float): Probability of being spam (0-100)
            - confidence_ham (float): Probability of being ham (0-100)
    """
    try:
        # Make prediction
        prediction = model.predict([message])[0]
        
        # Get probability scores
        probabilities = model.predict_proba([message])[0]
        
        # Extract probabilities for ham and spam
        # Note: classes are typically ordered alphabetically: ['ham', 'spam']
        classes = model.classes_
        prob_dict = dict(zip(classes, probabilities))
        
        confidence_ham = prob_dict.get('ham', 0) * 100
        confidence_spam = prob_dict.get('spam', 0) * 100
        
        return prediction, confidence_spam, confidence_ham
        
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None, 0, 0


def display_prediction_result(prediction, confidence_spam, confidence_ham):
    """
    Display prediction results with visual feedback.
    
    Args:
        prediction (str): 'spam' or 'ham'
        confidence_spam (float): Spam confidence percentage
        confidence_ham (float): Ham confidence percentage
    """
    st.markdown("---")
    st.subheader("📊 Prediction Result")
    
    if prediction == 'spam':
        # Display SPAM result with red warning style
        st.error("🚨 **SPAM DETECTED**")
        st.markdown(
            f"""
            <div style='padding: 20px; background-color: #ffebee; border-left: 5px solid #f44336; border-radius: 5px;'>
                <h3 style='color: #c62828; margin: 0;'>⚠️ This message is classified as SPAM</h3>
                <p style='color: #666; margin-top: 10px;'>This appears to be an unsolicited or potentially malicious message.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Display HAM result with green success style
        st.success("✅ **LEGITIMATE MESSAGE (HAM)**")
        st.markdown(
            f"""
            <div style='padding: 20px; background-color: #e8f5e9; border-left: 5px solid #4caf50; border-radius: 5px;'>
                <h3 style='color: #2e7d32; margin: 0;'>✓ This message appears to be legitimate</h3>
                <p style='color: #666; margin-top: 10px;'>This looks like a normal, non-spam message.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Display confidence scores
    st.markdown("### 📈 Confidence Scores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="🟢 Ham (Legitimate)",
            value=f"{confidence_ham:.2f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            label="🔴 Spam (Junk)",
            value=f"{confidence_spam:.2f}%",
            delta=None
        )
    
    # Visual progress bars
    st.markdown("#### Probability Distribution")
    st.progress(confidence_ham / 100, text=f"Ham: {confidence_ham:.1f}%")
    st.progress(confidence_spam / 100, text=f"Spam: {confidence_spam:.1f}%")


def main():
    """
    Main application function.
    """
    # App header
    st.title("📱 SMS Spam Classifier")
    st.markdown(
        """
        **Detect spam messages instantly using machine learning!**
        
        This application uses a TF-IDF + Multinomial Naive Bayes classifier trained on 
        5,500+ SMS messages to accurately identify spam and legitimate messages.
        """
    )
    
    # Try to load the model
    try:
        model = load_model('spam_model.joblib')
        model_loaded = True
    except FileNotFoundError:
        model_loaded = False
        st.error(
            """
            ❌ **Model file not found!**
            
            The trained model file `spam_model.joblib` doesn't exist.
            
            **Please follow these steps:**
            1. Open a terminal/command prompt
            2. Navigate to the project directory
            3. Run: `python train.py`
            4. Wait for training to complete
            5. Refresh this page
            """
        )
        st.stop()
    except Exception as e:
        model_loaded = False
        st.error(f"❌ **Error loading model:** {e}")
        st.stop()
    
    if model_loaded:
        st.success("✅ Model loaded successfully! Ready to classify messages.")
    
    # Add spacing
    st.markdown("---")
    
    # Example messages section
    st.markdown("### 💡 Try Example Messages")
    st.markdown("Click a button below to load an example message:")
    
    # Initialize session state for message if not exists
    if 'message_text' not in st.session_state:
        st.session_state.message_text = ""
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📨 Example Ham (Legitimate)", use_container_width=True):
            st.session_state.message_text = "Hi! Are you free for lunch today? Let me know what time works for you."
    
    with col2:
        if st.button("🚨 Example Spam (Junk)", use_container_width=True):
            st.session_state.message_text = "WINNER!! You have been selected to receive a £1000 cash prize! Call 09061701461 now to claim. Valid 12 hours only!"
    
    # Input section
    st.markdown("---")
    st.markdown("### ✍️ Enter Your Message")
    
    # Text input area - use session state directly as key
    user_message = st.text_area(
        label="Type or paste an SMS message to classify:",
        value=st.session_state.message_text,
        height=120,
        placeholder="Enter your SMS message here...\n\nExample: 'Free entry in 2 a wkly comp to win FA Cup final tkts'",
        help="Enter any SMS message to check if it's spam or legitimate (ham)"
    )
    
    # Update session state when user types
    st.session_state.message_text = user_message
    
    # Character count
    char_count = len(user_message)
    if char_count > 1000:
        st.warning(f"⚠️ Message is {char_count} characters long. Very long messages may affect prediction accuracy.")
    else:
        st.caption(f"Character count: {char_count}")
    
    # Classify button
    st.markdown("")
    classify_button = st.button("🔍 Classify Message", type="primary", use_container_width=True)
    
    # Perform classification when button is clicked
    if classify_button:
        if not user_message or user_message.strip() == "":
            st.warning("⚠️ Please enter a message to classify.")
        else:
            # Show processing spinner
            with st.spinner("🤖 Analyzing message..."):
                prediction, confidence_spam, confidence_ham = predict_message(model, user_message)
            
            if prediction:
                # Display results
                display_prediction_result(prediction, confidence_spam, confidence_ham)
    
    # Dataset Overview Section
    st.markdown("---")
    
    # Load and display dataset overview
    df = load_dataset('sms_spam_no_header.csv')
    if df is not None:
        display_dataset_overview(df)
    else:
        st.info("💡 Dataset file not found. Dataset visualizations are not available.")
    
    # Sidebar with information
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown(
        """
        ### How it works
        
        1. **Enter** an SMS message in the text area
        2. **Click** the "Classify Message" button
        3. **View** the prediction and confidence scores
        
        ### Model Details
        - **Algorithm**: Multinomial Naive Bayes
        - **Features**: TF-IDF Vectorization
        - **Accuracy**: ~96%
        - **Training Data**: 5,500+ SMS messages
        
        ### What is Spam?
        Spam messages are unsolicited, often commercial or malicious messages that you didn't ask for.
        
        ### What is Ham?
        Ham refers to legitimate, non-spam messages that are normal communications.
        
        ### Limitations
        - Trained on English SMS data only
        - May not detect sophisticated spam
        - Best for traditional SMS format
        """
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Built with Streamlit & scikit-learn")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p><strong>SMS Spam Classifier</strong> | Powered by Machine Learning</p>
            <p style='font-size: 0.9em;'>This tool is for educational purposes. Always use caution with suspicious messages.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
