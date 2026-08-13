import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
from ultralytics import YOLO
import tempfile
import av

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(page_title="لقمــــــة",
                    page_icon="🍛",
                    layout="wide")


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_yolo_model():

    return YOLO("best.pt")


try:

    model = load_yolo_model()

except Exception as e:

    st.error(
        f"Error loading model 'best.pt': {e}"
    )

    model = None




# ============================================================
# LIVE CAMERA FUNCTION
# ============================================================

class FoodVideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        # Get camera frame
        img = frame.to_ndarray(
            format='bgr24'
        )

        # Run YOLO
        if model is not None:

            results = model(
                img,
                verbose=False
            )

            # Draw boxes and labels
            annotated_frame = results[0].plot()

        else:

            annotated_frame = img

        # Return processed frame
        return av.VideoFrame.from_ndarray(
            annotated_frame,
            format='bgr24'
        )






# ============================================================
# COLORS AND STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       MAIN PAGE
       ========================= */

    .stApp {
        background-color: #F3EBDD;
        font-family: 'Georgia', serif;
    }


    /* =========================
       TEXT
       ========================= */

    h1, h2, h3, p,
    [data-testid="stMarkdownContainer"],
    [data-testid="stText"] {
        color: #582F0E !important;
        font-family: 'Georgia', serif !important;
    }


    /* =========================
       TABS
       ========================= */

    div[data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #656D4A;
        padding: 10px;
        border-radius: 16px;
    }

    button[data-baseweb="tab"] {
        background-color: #B6AD90;
        border: 2px solid #7F4F24;
        border-radius: 12px;
        padding: 10px 16px;
    }

    button[data-baseweb="tab"] p {
        color: #582F0E !important;
        font-size: 15px;
        font-weight: 600;
        font-family: 'Georgia', serif !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #7F4F24;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #B6AD90 !important;
    }

    button[data-baseweb="tab"]:hover {
        background-color: #582F0E;
    }

    button[data-baseweb="tab"]:hover p {
        color: #B6AD90 !important;
    }


    /* =========================
       BUTTONS
       ========================= */

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #B6AD90;
        color: #582F0E !important;
        border: 2px solid #7F4F24;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Georgia', serif !important;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #7F4F24;
        color: #B6AD90 !important;
        border-color: #582F0E;
    }


    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border: none;
        border-top: 2px solid #7F4F24;
        margin: 25px 0;
    }


    /* =========================
       TABLE
       ========================= */

    [data-testid="stTable"] table {
        width: 100%;
        border-collapse: collapse;
        border: 2px solid #7F4F24;
    }

    [data-testid="stTable"] th {
        background-color: #656D4A;
        color: #B6AD90 !important;
        border: 1px solid #7F4F24;
        padding: 12px;
        text-align: left;
    }

    [data-testid="stTable"] td {
        background-color: #B6AD90;
        color: #582F0E !important;
        border: 1px solid #7F4F24;
        padding: 12px;
    }


    /* =========================
       FILE UPLOADER
       ========================= */

    [data-testid="stFileUploader"] {
        border: 2px solid #7F4F24;
        border-radius: 12px;
        padding: 10px;
    }


    /* =========================
       SELECT BOX
       ========================= */

    div[data-baseweb="select"] > div {
        background-color: #B6AD90;
        border: 2px solid #7F4F24;
    }


    /* =========================
       DIVIDER
       ========================= */

    .element-container {
        color: #582F0E;
    }
    

    hr {
        border: none;
        border-top: 3px solid #656D4A;
        margin: 25px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# APP INFORMATION
# ============================================================

class_names = [
    'Chicken Machboos',
    'Balaleet',
    'Luqaimat',
    'Harees',
    'Regag Bread',
    'Sambosa',
    'Thareed',
    'Ghoozi',
    'Bahraini Halwa',
    'Tikka'
]


# ============================================================
# FOOD TABLE
# ============================================================

food_info = {
    'Food': [
        'Chicken Machboos',
        'Balaleet',
        'Luqaimat',
        'Harees',
        'Regag Bread',
        'Sambosa',
        'Thareed',
        'Ghoozi',
        'Bahraini Halwa',
        'Tikka'
    ],

    'Arabic Name': [
        'مكبوس الدجاج',
        'بلاليط',
        'لقيمات',
        'هريس',
        'خبز الرقاق',
        'سمبوسة',
        'ثريد',
        'قوزي',
        'حلوى بحرينية',
        'تكة'
    ]
}

food_table = pd.DataFrame(food_info)


# ============================================================
# TITLE
# ============================================================

st.title('🍛 Luqma')

st.subheader(
    'Where code meets cuisine, and your next favorite '
    'Bahraini meal is just a click away!'
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    '🏠 About Luqma',
    '🍛 Food Recognition',
    '📖 Bahraini Dishes'
])


# ============================================================
# TAB 1 - ABOUT LUQMA
# ============================================================

with tab1:

    st.header('Welcome to Luqma! 🍛')

    st.write('Luqma is an application that helps recognize '
             'different Bahraini dishes using image classification.')

    st.write('Upload a picture of a Bahraini dish and the model '
             'will try to identify what food it is.')

    st.markdown('---')

    st.subheader('🎥 About Bahraini Food')

    st.video('luqma.mp4')

    st.markdown('---')

    st.subheader('🇧🇭 Bahraini Dishes')

    st.write(
        'Here are some of the Bahraini dishes included in our application:'
    )

    st.table(food_table)


# ============================================================
# TAB 2 - FOOD RECOGNITION
# ============================================================

with tab2:

    st.header(' Food Recognition')

    st.write(
        'Upload an image of a Bahraini dish and Luqma '
        'will try to recognize it.'
    )

    st.markdown('---')


    # ========================================================
    # FOOD RECOGNITION OPTIONS
    # ========================================================

    option = st.radio(
        'Choose an option:',
        ['📁 Upload Image', '📷 Take a Picture',
         '🎥 Upload Video', '🎬 Record a Video']
    )


    # ========================================================
    # UPLOAD IMAGE
    # ========================================================

    if option == '📁 Upload Image':

        uploaded_file = st.file_uploader(
            'Upload a food image',
            type=['jpg', 'jpeg', 'png']
        )

        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            st.subheader('Your Image')

            st.image(
                image,
                caption='Uploaded Food Image',
                width=500
            )

            predict_button = st.button('🔍 Recognize Food')

            if predict_button:

                if model is not None:
                    with st.spinner('Analyzing image...'):
                        results = model(image)
                        res_plotted = results[0].plot()
                        st.subheader('Detection Result')
                        st.image(
                            res_plotted,
                            caption='Recognized Food',
                            width=500
                        )
                else:
                    st.error("Model 'best.pt' is not loaded properly.")

        else:

            st.write(
                'Please upload an image to start food recognition.'
            )


    # ========================================================
    # TAKE A PICTURE
    # ========================================================

    elif option == '📷 Take a Picture':

        camera_image = st.camera_input(
            'Take a picture of your food'
        )

        if camera_image is not None:

            image = Image.open(camera_image)

            st.subheader('Your Image')

            st.image(
                image,
                caption='Camera Image',
                width=500
            )

            predict_button = st.button('🔍 Recognize Food')

            if predict_button:

                if model is not None:
                    with st.spinner('Analyzing captured image...'):
                        results = model(image)
                        res_plotted = results[0].plot()
                        st.subheader('Detection Result')
                        st.image(
                            res_plotted,
                            caption='Recognized Food',
                            width=500
                        )
                else:
                    st.error("Model 'best.pt' is not loaded properly.")

        else:

            st.write(
                'Take a picture to start food recognition.'
            )




# ============================================================
# TAB 3 - BAHRAINI DISHES
# ============================================================

with tab3:

    st.header('📖 Bahraini Dishes')

    st.write(
        'Choose a Bahraini dish to learn more about it.'
    )

    st.markdown('---')

    selected_food = st.selectbox(
        'Choose a dish:',
        class_names
    )


    # ========================================================
    # FOOD INFORMATION
    # ========================================================

    if selected_food == 'Chicken Machboos':

        st.subheader('🍗 Chicken Machboos')

        st.write(
            'A traditional Bahraini rice dish prepared '
            'with chicken and aromatic spices.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Chicken'
            '\n- Basmati rice'
            '\n- Onion'
            '\n- Tomato'
            '\n- Garlic'
            '\n- Bahraini spices'
            '\n- Dried lemon'
            '\n- Oil'
            '\n- Salt'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'First, cook the chicken with the onion, tomato, '
            'garlic and spices. Then add water and rice and '
            'cook everything together until the rice is soft '
            'and the chicken is fully cooked.'
        )


    if selected_food == 'Balaleet':

        st.subheader('🍜 Balaleet')

        st.write(
            'A traditional sweet and savory dish made '
            'with vermicelli and eggs.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Vermicelli'
            '\n- Eggs'
            '\n- Sugar'
            '\n- Cardamom'
            '\n- Saffron'
            '\n- Rose water'
            '\n- Butter'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Cook the vermicelli with sugar and spices. '
            'Prepare the eggs separately and serve them '
            'with the sweet vermicelli.'
        )


    if selected_food == 'Luqaimat':

        st.subheader('🍯 Luqaimat')

        st.write(
            'Small sweet dumplings that are usually served '
            'with date syrup or honey.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Flour'
            '\n- Yeast'
            '\n- Sugar'
            '\n- Water'
            '\n- Cardamom'
            '\n- Oil'
            '\n- Date syrup or honey'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Mix the ingredients to make a soft batter. '
            'Leave the batter to rest, then form small pieces '
            'and fry them in hot oil. Finally, serve with '
            'date syrup or honey.'
        )


    if selected_food == 'Harees':

        st.subheader('🥣 Harees')

        st.write(
            'A traditional dish made mainly from wheat '
            'and meat.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Wheat'
            '\n- Meat or chicken'
            '\n- Water'
            '\n- Salt'
            '\n- Butter or ghee'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Cook the wheat and meat together until they '
            'become very soft. Mix and mash them until the '
            'mixture becomes smooth, then add butter or ghee.'
        )


    if selected_food == 'Regag Bread':

        st.subheader('🫓 Regag Bread')

        st.write(
            'A very thin traditional Bahraini bread.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Flour'
            '\n- Water'
            '\n- Salt'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Mix the flour, water and salt to make a thin '
            'batter. Spread the batter very thinly on a hot '
            'surface and cook until the bread is ready.'
        )


    if selected_food == 'Sambosa':

        st.subheader('🥟 Sambosa')

        st.write(
            'A crispy pastry filled with different fillings '
            'such as meat, cheese or vegetables.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Sambosa pastry'
            '\n- Minced meat or vegetables'
            '\n- Onion'
            '\n- Spices'
            '\n- Oil'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Prepare the filling with onion and spices. '
            'Place the filling inside the pastry and fold it. '
            'Fry the sambosa until it becomes golden and crispy.'
        )


    if selected_food == 'Thareed':

        st.subheader('🍲 Thareed')

        st.write(
            'A traditional dish made with thin bread and '
            'a flavorful stew.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Regag bread'
            '\n- Meat or chicken'
            '\n- Potato'
            '\n- Tomato'
            '\n- Onion'
            '\n- Vegetables'
            '\n- Spices'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Prepare the meat or chicken with vegetables, '
            'tomato and spices to make a stew. Place pieces '
            'of regag bread in a serving dish and pour the '
            'stew over the bread.'
        )


    if selected_food == 'Ghoozi':

        st.subheader('🍖 Ghoozi')

        st.write(
            'A traditional Gulf dish usually prepared '
            'with rice and roasted meat.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Lamb or meat'
            '\n- Rice'
            '\n- Onion'
            '\n- Spices'
            '\n- Nuts'
            '\n- Raisins'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Season and cook the meat until tender. Prepare '
            'the rice with onions and spices, then serve the '
            'meat on top of the rice and add nuts and raisins.'
        )


    if selected_food == 'Bahraini Halwa':

        st.subheader('🍮 Bahraini Halwa')

        st.write(
            'A traditional Bahraini sweet known for its '
            'rich texture and flavor.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Sugar'
            '\n- Corn starch'
            '\n- Water'
            '\n- Saffron'
            '\n- Cardamom'
            '\n- Rose water'
            '\n- Oil or butter'
            '\n- Nuts'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Mix the ingredients together and cook them over '
            'low heat while stirring continuously until the '
            'mixture becomes thick. Add nuts and spices, then '
            'serve when ready.'
        )


    if selected_food == 'Tikka':

        st.subheader('🍢 Tikka')

        st.write(
            'Seasoned pieces of meat that are grilled '
            'and commonly enjoyed in Bahrain.'
        )

        st.markdown('---')

        st.subheader('🥘 Ingredients')

        st.write(
            '- Meat'
            '\n- Onion'
            '\n- Garlic'
            '\n- Lemon juice'
            '\n- Spices'
            '\n- Salt'
            '\n- Oil'
        )

        st.subheader('👩🏻‍🍳 How to Prepare')

        st.write(
            'Cut the meat into small pieces and marinate it '
            'with onion, garlic, lemon juice and spices. '
            'Place the meat on skewers and grill until fully '
            'cooked.'
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.subheader('🍛 Luqma')

    st.write(
        'Bahraini Food Recognition App'
    )

    st.markdown('---')

    st.write(
        'Choose a tab above to explore the application.'
    )