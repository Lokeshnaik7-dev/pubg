import streamlit as st

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Social App", layout="wide")

# ------------------ SMARTLINK ------------------
SMARTLINK_URL = "https://omg10.com/4/10948862"  # your monetag smartlink

def smartlink_button(text="🔥 Unlock Content"):
    st.markdown(
        f"""
        <a href="{SMARTLINK_URL}" target="_blank">
            <button style="
                background-color:#ff4b4b;
                color:white;
                padding:10px 20px;
                border:none;
                border-radius:8px;
                cursor:pointer;
                font-size:16px;">
                {text}
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# ------------------ SESSION STATE ------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "users" not in st.session_state:
    st.session_state.users = {}

if "posts" not in st.session_state:
    st.session_state.posts = []

if "page" not in st.session_state:
    st.session_state.page = "login"

# ------------------ AUTH ------------------
def login():
    st.title("🔐 Login")

    smartlink_button("🎬 Continue to App")  # optional earning point

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.user = username
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()


def signup():
    st.title("📝 Create Account")

    smartlink_button("🎁 Unlock Signup Bonus")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    dp = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])

    if st.button("Sign Up"):
        if username not in st.session_state.users:
            st.session_state.users[username] = {
                "password": password,
                "dp": dp
            }
            st.success("Account created!")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("User already exists")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# ------------------ MAIN APP ------------------
def main_app():
    user = st.session_state.user
    user_data = st.session_state.users[user]

    # -------- Sidebar --------
    st.sidebar.title("👤 Profile")

    if user_data["dp"]:
        st.sidebar.image(user_data["dp"], width=100)

    st.sidebar.write(f"**{user}**")

    st.sidebar.markdown("### 🎬 Sponsored")
    smartlink_button("▶ Watch & Earn")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    # -------- SEARCH PROFILES --------
    st.title("🔍 Search Profiles")

    search_query = st.text_input("Search username")

    if search_query:
        matched_users = [
            u for u in st.session_state.users
            if search_query.lower() in u.lower()
        ]

        if matched_users:
            for u in matched_users:
                col1, col2 = st.columns([1, 6])

                if st.session_state.users[u]["dp"]:
                    col1.image(st.session_state.users[u]["dp"], width=50)

                col2.write(f"**{u}**")
        else:
            st.warning("No users found")

    st.divider()

    # -------- Upload Section --------
    st.title("📹 Upload Video")

    video = st.file_uploader("Upload Video", type=["mp4", "mov"])
    caption = st.text_input("Caption")

    if st.button("Post"):
        if video:
            post = {
                "user": user,
                "video": video,
                "caption": caption,
                "likes": 0,
                "comments": [],
                "shares": 0,
                "subscribers": []
            }
            st.session_state.posts.insert(0, post)
            st.success("Posted!")
            st.rerun()

    st.divider()

    # -------- Feed --------
    st.title("🔥 Feed")

    for i, post in enumerate(st.session_state.posts):
        col1, col2 = st.columns([1, 8])

        if st.session_state.users[post["user"]]["dp"]:
            col1.image(st.session_state.users[post["user"]]["dp"], width=50)

        col2.write(f"**{post['user']}**")
        col2.write(post["caption"])

        st.video(post["video"])

        # 💰 BEST earning position
        smartlink_button("🔓 Unlock Next Video")

        # -------- Actions --------
        c1, c2, c3, c4 = st.columns(4)

        if c1.button(f"❤️ {post['likes']}", key=f"like{i}"):
            post["likes"] += 1
            st.rerun()

        if c2.button(f"💬 {len(post['comments'])}", key=f"comment{i}"):
            comment = st.text_input("Add comment", key=f"text{i}")
            if st.button("Send", key=f"send{i}"):
                post["comments"].append(f"{user}: {comment}")
                st.rerun()

        if c3.button(f"🔁 {post['shares']}", key=f"share{i}"):
            post["shares"] += 1
            st.rerun()

        if c4.button("➕ Subscribe", key=f"sub{i}"):
            if user not in post["subscribers"]:
                post["subscribers"].append(user)
                st.success("Subscribed!")
            else:
                st.info("Already subscribed")

        for c in post["comments"]:
            st.write("💬", c)

        st.divider()


# ------------------ ROUTING ------------------
if st.session_state.user:
    main_app()
else:
    if st.session_state.page == "login":
        login()
    else:
        signup()
