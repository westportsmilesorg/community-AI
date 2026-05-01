import json
import os
import streamlit as st
from PIL import Image
import random
import base64
import io
from openai import OpenAI

def show_footer():
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f9f9f9;
        color: #555;
        text-align: center;
        padding: 10px 0;
        font-size: 13px;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }
    .footer a {
        color: #0066cc;
        text-decoration: none;
        font-weight: 500;
        margin: 0 6px;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        © 2026 Westport Smiles. All rights reserved |
        <a href="?page=legal">Legal Disclaimer</a> |
        Contact us:
        <a href="mailto:westportsmiles.org@gmail.com">
            westportsmiles.org@gmail.com
        </a>
    </div>
    """, unsafe_allow_html=True)

# ================== ENV & OPENAI ==================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# ================== PAGE STATE ==================
if "page" not in st.session_state:
    st.session_state.page = "landing"
    
query_params = st.query_params

if "page" in query_params and st.session_state.page == "landing":
    st.session_state.page = query_params["page"]
    
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ================== USERS ==================
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ================== AI FUNCTIONS (MERGED) ==================
def image_to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def detect_object(image: Image.Image) -> str:
    img64 = image_to_base64(image)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Identify the main object. Only 1-3 words."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img64}"}
                }
            ]
        }],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def kindness_ideas(object_name: str) -> str:
    prompt = f"""
You are helping a local community improve social interaction.
The object identified is: {object_name}

Generate 3–5 meaningful ideas for being kind when using this object.
They must be kind, nice, and easy for kids to understand.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()
# ================= legal page =================
if st.session_state.page == "legal":
    st.title("Legal Disclaimer & Technology Disclosure")

    st.markdown("""

### 🔬 Beta Platform & AI Usage
This website is currently in **Beta** and serves as an experimental platform for our mission.  
To help us build bridges and generate smiles more efficiently, we utilize various third-party artificial intelligence and web technologies, including tools provided by **OpenAI, Google, and Streamlit**.

---

### 🔍 Transparency & Independent Policy

#### 🧭 Independent Policies
We are an independent entity. Our organizational policies, mission, and content standards are **distinct** from those of our technology providers (including OpenAI, Google, and Streamlit).  
Your interaction with our site is governed by **our own terms**, not the terms of our software vendors.

#### ⚠️ Accuracy & Human Oversight
Although we use AI to assist in our work, our team strives to oversee and curate the content provided.  
AI-generated content can occasionally be **incorrect or incomplete**. Please verify any critical information independently before relying upon it.

#### 📘 Nature of Information
Content on this site is provided for **general informational purposes only** and does **not** constitute professional, legal, medical, or financial advice.

#### ⚖️ Limitation of Liability
By using this site, you acknowledge that you are using these tools at your own discretion and risk.  
**Westport Smiles and its affiliates are not liable** for any damages or losses resulting from your reliance on the information or services provided here.

---

### 💙 Our Commitment
We are using code to build bridges and spread positivity.  
We appreciate your patience and feedback as we continue to test and refine this technology to better serve our community.

---

### 🔗 Learn More
For more information on the platforms that power our development, you may review:

- OpenAI Usage Policies  
- Google AI Principles  
- Streamlit Terms of Service  

""")

    if st.button("⬅ Back to Home"):
        st.query_params.clear() 
        st.session_state.page = "landing"
        st.rerun()

    show_footer()
    st.stop()
# ================= LANDING PAGE =================
if st.session_state.page == "landing":
    st.image("westport.png", use_container_width=True)

    st.title("Westport Smiles 😊")
    st.subheader("A Kindness Project : See an Object, Spark a Connection! ")

    st.markdown("""
    Join us—Lisette, Leonie, and Professor Juju—as we use AI to fight the loneliness epidemic by turning everyday objects into sparks for human connection. 
                        Our mission is to help everyone, from kids to seniors, break down barriers and "Be Best" through small acts of kindness that foster a healthier community.
                We invite you to explore our project, where we merge technology with real-world interaction to ensure no one has to feel like they are on a "lonely island" anymore.
    """)

    st.markdown("""
    📸 Upload or take a photo  
    💖 Get kind ideas  
    🌍 Make your community happier  
    """)

    # st.markdown("###")  # spacing

    col_try, col_space = st.columns([1, 3])
    with col_try:
        if st.button("🚀 Try the App", use_container_width=True):
            st.session_state.page = "app"
            st.rerun()


    st.markdown("### Explore")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🎥 AI App Demo"):
            st.session_state.page = "video"
            st.rerun()

    with col2:
        if st.button("🎬 Animated Video"):
            st.session_state.page = "animated_video"
            st.rerun()

    with col3:
        if st.button("📚 Responsible AI"):
            st.session_state.page = "Responsible AI"
            st.rerun()
            
    with col4:
        if st.button("📰 In the news"):
            st.session_state.page = "news"
            st.rerun()
            
    show_footer()
    st.stop()
    # ================= CHANGE PASSWORD PAGE =================


if st.session_state.page == "change_password":

    st.title("🔐 Change Password")

    current_pwd = st.text_input("Current Password", type="password")
    new_pwd = st.text_input("New Password", type="password")
    confirm_pwd = st.text_input("Confirm New Password", type="password")

    users = load_users()
    username = st.session_state.username

    if st.button("Update Password"):
        if users.get(username) != current_pwd:
            st.error("Current password is incorrect")
        elif new_pwd != confirm_pwd:
            st.error("New passwords do not match")
        elif len(new_pwd) < 4:
            st.error("Password should be at least 4 characters")
        else:
            users[username] = new_pwd
            save_users(users)
            st.success("Password updated successfully 🎉")

    if st.button("⬅ Back to App"):
        st.session_state.page = "app"
        st.rerun()
    show_footer()
    st.stop()
# ================= APP PAGE =================
# if st.session_state.page == "app":

#     # ---------- SIDEBAR ----------
#     #st.sidebar.write(f"👋 Hello, {st.session_state.username}")
#     st.sidebar.write("👋 Welcome!")

#     # ---------- APP HEADER ----------
#     col_logo, col_title = st.columns([1, 5])

#     with col_logo:
#         st.image("kindness_logo.png", width=80)

#     with col_title:
#         st.markdown("## Westport Smiles 😊")

#     st.info(random.choice([
#         "Say I love you to a loved one.",
#         "Smile at a stranger.",
#         "Give a friend a compliment.",
#         "Approach things with a positive attitude."
#     ]))

#     st.markdown("Upload or take a photo of an object")

#     mode = st.radio("Choose image source", ["Upload", "Camera"])

#     image = None

#     if mode == "Upload":
#         uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
#         if uploaded:
#             image = Image.open(uploaded)

#     else:
#         cam = st.camera_input("Take a photo")
#         if cam:
#             image = Image.open(cam)

#     if image:
#         st.image(image, caption="Your Image", use_container_width=True)

#         if st.button("Kindness Starts Here"):
#             with st.spinner("Thinking kindly..."):
#                 obj = detect_object(image)
#                 ideas = kindness_ideas(obj)

#             st.subheader(f"🧠 Object: {obj}")
#             st.subheader("🌟 Kindness Ideas")

#             for idea in ideas.split("\n"):
#                 if idea.strip():
#                     st.write("•", idea)

#     if st.button("⬅ Back to Home"):
#         st.session_state.page = "landing"
#         st.rerun()
#     show_footer()    
#     st.stop()
# ================= APP PAGE =================
if st.session_state.page == "app":

    # ---------- SESSION STATE INIT ----------
    if "image" not in st.session_state:
        st.session_state.image = None

    if "input_source" not in st.session_state:
        st.session_state.input_source = None  # "upload" or "camera"

    # ---------- SIDEBAR ----------
    st.sidebar.write("👋 Welcome!")

    # ---------- HEADER ----------
    col_logo, col_title = st.columns([1, 5])

    with col_logo:
        st.image("kindness_logo.png", width=80)

    with col_title:
        st.markdown("## Westport Smiles 😊")

    st.info(random.choice([
        "Say I love you to a loved one.",
        "Smile at a stranger.",
        "Give a friend a compliment.",
        "Approach things with a positive attitude."
    ]))

    st.markdown("Upload or take a photo of an object")

    # ---------- INPUT MODE ----------
    mode = st.radio("Choose image source", ["Upload", "Camera"])

    # ---------- IMAGE INPUT ----------
    if mode == "Upload":
        uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

        if uploaded:
            st.session_state.image = Image.open(uploaded)
            st.session_state.input_source = "upload"

            # ✅ Only show image manually for upload
            st.image(st.session_state.image, caption="Your Image", use_container_width=True)

    else:
        cam = st.camera_input("Take a photo")

        if cam:
            st.session_state.image = Image.open(cam)
            st.session_state.input_source = "camera"
            # ❌ Do NOT call st.image() → camera already shows preview

    # ---------- PROCESS ----------
    if st.session_state.image is not None:
        if st.button("Kindness Starts Here"):
            with st.spinner("Thinking kindly..."):
                obj = detect_object(st.session_state.image)
                ideas = kindness_ideas(obj)

            st.subheader(f"🧠 Object: {obj}")
            st.subheader("🌟 Kindness Ideas")

            for idea in ideas.split("\n"):
                if idea.strip():
                    st.write("•", idea)

            # ✅ Reset after processing
            st.session_state.image = None
            st.session_state.input_source = None

    # ---------- CLEAR BUTTON ----------
    if st.session_state.image is not None:
        if st.button("🗑 Clear Image"):
            st.session_state.image = None
            st.session_state.input_source = None
            st.rerun()

    # ---------- NAVIGATION ----------
    if st.button("⬅ Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

    show_footer()
    st.stop()    

# ================= VIDEO PAGE =================

if st.session_state.page == "video":
    st.title("🎥 Westport Smiles – Demo Video")
    #st.video("demo_video.mp4")
 
    st.markdown(
        """
        <iframe 
            src="https://drive.google.com/file/d/1uMMOggdCbPsxMTtAtL976lLQngDGqIFq/preview"
            width="100%"
            height="480"
            allow="autoplay">
        </iframe>
        """,
        unsafe_allow_html=True
    )

    if st.button("⬅ Back to Home"):
        st.session_state.page = "landing"
        st.rerun()
    show_footer()    
    st.stop()

# ================= ANIMATED VIDEO PAGE =================
if st.session_state.page == "animated_video":
    st.title("🎬 Westport Smiles – Animated Video")

    st.markdown(
        """
        <iframe 
            src="https://drive.google.com/file/d/1WbEeFdCUM-eIp2Xsd6gM24Di_GbCAnVC/preview"
            width="100%"
            height="480"
            allow="autoplay">
        </iframe>
        """,
        unsafe_allow_html=True
    )
    if st.button("⬅ Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

    show_footer()
    st.stop()


# ================= RESOURCES PAGE =================
if st.session_state.page == "Responsible AI":
    st.title("📚 Professor Juju's AI resources")

    st.markdown("""
- **U.S. National Artificial Intelligence Initiative (ai.gov)**  
  https://www.ai.gov/  
  Official U.S. government site with AI strategies, trustworthy AI, and youth education initiatives.
 
- **Presidential AI Challenge**  
  https://www.ai.gov/initiatives/presidential-challenge  
  White House-backed national challenge for K-12 kids and educators to build positive, responsible AI projects solving real problems.
 
- **Advancing Artificial Intelligence Education for American Youth**  
  https://www.whitehouse.gov/presidential-actions/2025/04/advancing-artificial-intelligence-education-for-american-youth/  
  Executive Order promoting AI education, professional development, and access for American students.
 
- **U.S. Department of Education: Artificial Intelligence Guidance**  
  https://www.ed.gov/about/ed-overview/artificial-intelligence-ai-guidance  
  Federal resources on safe, innovative, and responsible AI use in education.
 
- **Khan Academy: AI for Education**  
  https://www.khanacademy.org/college-careers-more/ai-for-education  
  Free lessons, videos, and tools on AI basics, ethics, biases, and responsible teaching/learning.
 
- **Khan Academy's Framework for Responsible AI in Education**  
  https://blog.khanacademy.org/khan-academys-framework-for-responsible-ai-in-education/  
  Clear principles for safe, fair, and equitable AI in schools and learning.
 
- **Common Sense Education AI Literacy Lessons**  
  https://www.commonsense.org/education/collections/ai-literacy-lessons-for-grades-6-12  
  Quick, fun lessons on AI ethics, biases, and responsible use.
 
- **Code.org: Teach and Learn AI**  
  https://code.org/en-US/artificial-intelligence  
  Hands-on projects teaching kids ethical and thoughtful AI.
 
- **MIT Media Lab: AI + Ethics Curriculum for Middle School**  
  https://www.media.mit.edu/projects/ai-ethics-for-middle-school/overview/  
  Free lessons on fairness, biases, and ethical AI thinking.
 
- **TeachAI: AI Guidance for Schools Toolkit**  
  https://www.teachai.org/toolkit  
  Practical resources for promoting responsible AI in education.
 
- **Family Online Safety Institute: Teaching Kids About AI**  
  https://fosi.org/teaching-kids-about-ai-a-parents-guide-to-curiosity-and-critical-thinking/  
  Guide for families to explore AI safely and critically.
 
- **Understood.org: How to Use AI Responsibly**  
  https://www.understood.org/en/articles/ai-responsible-use-students  
  Kid- and family-friendly tips on honest, safe, and fair AI use.                                       
""")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

    show_footer()    
    st.stop()
# ================= NEWS PAGE =================
if st.session_state.page == "news":
    st.title("📰 Westport Smiles – In the News")

    st.markdown("""


### 📰 Media Coverage

- **CT Insider Article**  
  https://www.ctinsider.com/westport/article/westport-smiles-app-loneliness-connections-22218628.php  

- **News 12 Feature**  
  https://news12.com/11-year-old-westport-twins-create-ai-website-to-combat-loneliness-epidemic-help-spread-kindness  

- **Westport Journal Article**  
  https://westportjournal.com/community/westports-kalra-twins-advance-in-ai-challenge-with-kindness-app/  

- **Melissa in the Morning**  
  https://audioboom.com/posts/8895942-melissa-in-the-morning-westport-smiles?fbclid=IwZnRzaARcwIZleHRuA2FlbQIxMQBzcnRjBmFwcF9pZAo2NjI4NTY4Mzc5AAEe6xwe9OSyRDEnlVGRZK1JsTQnD-wFLWJyPuCHJbeNqf3tvMwCwQIhryZOopY_aem_Zb4-Q-6C1-WT461JzMnsiA

- **2026 Predential AI state champions**  
  https://orise.orau.gov/ai-challenge/winners/2026/state.html
                
- **Congratulations to 2026 NASSC Winners**  
  https://www.scrabblechampionship.com/standings
                

### 🌐 Explore the Project

- **Live Platform**  
  https://westportsmiles.org  

- **Upcoming Initiative – America Smiles (501(c)(3))**  
  https://americasmiles.org  

---

### ❤️ Proud Moment

We are incredibly proud of the hard work, creativity, and impact Lisette and Leonie are making in their community.

🏆 **Presidential AI Challenge Achievement**  
Lisette and Leonie proudly represented **Connecticut** and secured **1st place in the Middle School Technical Division** of the Presidential AI Challenge.  
Their project reflects innovation, compassion, and a strong commitment to using technology for good.

🎉 **National Scrabble Championship Success**  
Lisette and Leonie, known as the **"Pink Fluffy Unicorns"**, also earned a **Silver Medal** at the prestigious **North American School Scrabble Championship** held in Washington, D.C.  

🔗 **Learn more about their achievement:**
  Please visit the official Championship Standings and read up on the history of the events.  
- https://www.scrabblechampionship.com/standings  
- https://en.wikipedia.org/wiki/North_American_School_Scrabble_Championship
- https://www.yahoo.com/lifestyle/articles/westport-twin-sisters-create-app-100000010.html  
- https://www.msn.com/en-us/lifestyle/parenting/westport-twin-sisters-create-app-that-uses-ai-to-create-ideas-on-how-to-connect-with-others/ar-AA21y7BV

---

✨ *Please join us in celebrating these amazing milestones and the positive difference they are making!*
""")


    if st.button("⬅ Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

    show_footer()
    st.stop()

