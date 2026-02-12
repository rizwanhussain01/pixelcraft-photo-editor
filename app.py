import streamlit as st
import numpy as np
import cv2
import filters as ft
import adjustments as ad
import transform as tf
import draw as dr
from streamlit_cropper import st_cropper
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates


st.markdown("<h1 style='text-align:center;'>🎨 PixelCraft – Photo Editor</h1>",unsafe_allow_html=True)
def toast(msg):
    st.toast(f"✅ {msg}")

if "upload_toast_shown" not in st.session_state:
    st.session_state.upload_toast_shown = False

if "last_values" not in st.session_state:
    st.session_state.last_values = {}

def toast_if_changed(key,value,message):
    if key not in st.session_state.last_values:
        st.session_state.last_values[key] = value
        return
    
    if st.session_state.last_values[key]!= value:
        toast(message)
        st.session_state.last_values[key] = value

file = st.file_uploader("", type=["jpeg","png","jpg"], label_visibility="collapsed")

if "crop_mode" not in st.session_state:
    st.session_state.crop_mode = False

if "temp_crop" not in st.session_state:
    st.session_state.temp_crop = None

if file is not None:
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    if "edited_image" not in st.session_state:
        st.session_state.edited_image = image.copy()
    edited_image = st.session_state.edited_image

    if not st.session_state.upload_toast_shown:
        st.toast("Image uploaded successfully ✅")
        st.session_state.upload_toast_shown = True
    
    st.sidebar.header("🎨 Color Filter") 
    filter_choice = st.sidebar.selectbox("Choose Color Filter", ["None","Grayscale (Black & White)", "Invert (Negative)", "Red Channel" , "Green Channel", "Blue Channel"])

    if filter_choice == "Grayscale (Black & White)":
        edited_image = ft.grayscale(edited_image)
    
    elif filter_choice == "Invert (Negative)":
        edited_image = ft.invert(edited_image)
        
    elif filter_choice == "Red Channel":
        edited_image = ft.red_channel(edited_image)
       
    elif filter_choice == "Green Channel":
        edited_image = ft.green_channel(edited_image)
        
    elif filter_choice == "Blue Channel":
        edited_image = ft.blue_channel(edited_image)
        
    else:
        pass

    toast_if_changed("filter", filter_choice,f"{filter_choice} applied")
    st.sidebar.divider()
    st.sidebar.header("🌫️ Blur Effect")
    blur_choice = st.sidebar.selectbox("Choose Blur Effect", ["None","Normal Blur", "Gaussian Blur", "Median Blur"])

    if blur_choice == "Normal Blur":
        k = st.sidebar.slider("Normal Blur Level", min_value=1 , max_value=51, step=2)
        edited_image = ft.normal_blur(edited_image,k)
    elif blur_choice == "Gaussian Blur":
        k = st.sidebar.slider("Gaussian Blur Level", min_value=1 , max_value=51, step=2)
        edited_image = ft.gaussian_blur(edited_image,k)
    elif blur_choice == "Median Blur":
        k = st.sidebar.slider("Median Blur Level", min_value=3 , max_value=21, step=2)
        edited_image = ft.median_blur(edited_image,k)
    else:
        pass
    
    toast_if_changed("blur",blur_choice, f"{blur_choice} applied")
    st.sidebar.divider()
    st.sidebar.header("🔆 Adjust Image")
    bl = st.sidebar.slider("Brightness Level",-100,100,0,1 )
    edited_image = ad.adjust(edited_image, bl)
    toast_if_changed("brightness",bl, f"Brightness: {bl}")
    cl = st.sidebar.slider("Contrast Level",-100, 100, 1)
    edited_image = ad.adjust(edited_image, cl)
    toast_if_changed("contrast",cl, f"Contrast: {cl}")

    st.sidebar.divider()
    st.sidebar.header("🔄 Transform")
    rp = st.sidebar.slider("Image Size (%)", 5,300,100,1)
    edited_image = tf.resize(edited_image,rp)
    toast_if_changed("scale",rp,f"Resized to {rp}%")
    st.sidebar.caption(f"Current Scale: {rp}%")

    
    rl = st.sidebar.slider("Rotation angle", -180,180,0,1)
    edited_image = tf.rotate(edited_image,rl)
    toast_if_changed("rotate",rl, f"Rotated {rl}°")

    
    
    flip_choice = st.sidebar.radio("Flip Direction", ["None","Horizontal" , "Vertical"])
    if flip_choice == "Horizontal":
        edited_image = tf.horizontal_flip(edited_image)
    elif flip_choice == "Vertical":
        edited_image = tf.vertical_flip(edited_image)
    else:
        pass

    toast_if_changed("flip",flip_choice, f"Flipped {flip_choice}")  

    st.sidebar.divider()
    st.sidebar.header("✂️ Crop")
    if not st.session_state.crop_mode:
        if st.sidebar.button("Start Crop"):
            st.session_state.crop_mode = True
            st.rerun()

    

    if st.session_state.crop_mode:
        rgb_image = cv2.cvtColor(st.session_state.edited_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        cropped_pil = st_cropper(pil_image,realtime_update=True,box_color="red",aspect_ratio=None)
        cropped_np = np.array(cropped_pil)
        st.session_state.temp_crop = cv2.cvtColor(cropped_np,cv2.COLOR_RGB2BGR)

    if st.session_state.crop_mode:
        st.sidebar.caption("Drag to select area, then click Apply Crop")

        if st.sidebar.button("Apply Crop"):
            st.session_state.edited_image = st.session_state.temp_crop.copy()
            st.session_state.crop_mode = False
            st.session_state.temp_crop = None
            st.rerun()

        if st.sidebar.button("Cancel Crop"):
            st.session_state.crop_mode = False
            st.session_state.temp_crop = None
            st.rerun()

    st.sidebar.divider()
    st.sidebar.header("✏️ Draw")
    if "draw_mode" not in st.session_state:
        st.session_state.draw_mode = None

    add_shape = st.sidebar.button("Add Shape")
    if add_shape:
        st.session_state.draw_mode = "menu"
        st.sidebar.caption("🖱️ Click two points to draw shape")


    if st.session_state.draw_mode == "menu":
        choose_shape = st.sidebar.selectbox("Choose Shape", ["None","Line","Rectangle/Square", "Circle"])

        if choose_shape == "Line":
            st.session_state.draw_mode = "line"

        elif choose_shape == "Rectangle/Square":
            st.session_state.draw_mode = "rectangle"

        elif choose_shape == "Circle":
            st.session_state.draw_mode = "circle"


        else:
            pass

    if st.session_state.draw_mode == "line":
        with st.sidebar.expander("📏 Line Settings", expanded=True):
            color_hex = st.color_picker("Pick a Color", "#00ff00")
            thickness = st.slider("Shape Thickness",1,30,3)
        st.session_state.edited_image = dr.draw_line(st.session_state.edited_image,color_hex,thickness)

    if st.session_state.draw_mode == "rectangle":
        with st.sidebar.expander("⬛ Rectangle Settings", expanded=True):
            color_hex = st.color_picker("Pick a Color", "#00ff00")
            thickness = st.slider("Shape Thickness",1,30,3)
            filled = st.toggle("Filled Shape", False)
        st.session_state.edited_image = dr.draw_rect(st.session_state.edited_image,color_hex,thickness,filled)

    if st.session_state.draw_mode == "circle":
        with st.sidebar.expander("⚪ Circle Settings", expanded=True):
            color_hex = st.color_picker("Pick a Color", "#00ff00")
            thickness = st.slider("Shape Thickness",1,30,3)
            filled = st.toggle("Filled Shape", False)
            radius = st.slider("Radius",5,500,80)
        st.session_state.edited_image = dr.draw_circle(st.session_state.edited_image,color_hex,thickness,filled,radius)

    if "text_mode" not in st.session_state:
        st.session_state.text_mode = False
    

    if st.sidebar.button("Add Text"):
        st.session_state.text_mode = True
    
    if st.session_state.text_mode:
        st.sidebar.caption("Click on the image to place text")
        with st.sidebar.expander("📝 Text Settings", expanded=True):
            user_text = st.text_input("Enter Text","Hello")
            font_name = st.selectbox("Select Font", ["Simplex","Plain","Duplex","Complex","Triplex","Complex Small","Script Simplex","Script Complex"])
            font_scale = st.slider("Font Size",0.5,30.0,5.5)
            thickness = st.slider("Text Thickness",1,30,5)
            color_hex = st.color_picker("Text Color", "#00ff00")

        st.session_state.edited_image = dr.draw_text(st.session_state.edited_image,user_text,font_name,font_scale,thickness,color_hex)

   
    col1, col2 = st.columns(2)

    with col1:
        st.header("Original Image")
        with st.container(border=True):
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), width="content")
        st.caption("Tip: Use tools from sidebar to edit the image")


    with col2:
        st.header("Edited Image")
        h,w = edited_image.shape[:2]
        orig_h, orig_w = image.shape[:2]
        with st.container(border=True):
            st.image(cv2.cvtColor(edited_image, cv2.COLOR_BGR2RGB), width="content")
        percent_w = (w/orig_w)*100
        percent_h = (h/orig_h)*100
        c1,c2 = st.columns(2)
        c1.metric("Width", f"{w}px")
        c2.metric("Height", f"{h}px")

 
    st.divider()
    if "save_mode" not in st.session_state:
        st.session_state.save_mode = False


    if st.button("💾 Save Image"):
        st.session_state.save_mode = True

    if st.session_state.save_mode:

        col_a, col_b, col_c = st.columns([2,2,1])

        with col_a:
            file_name = st.text_input("File Name", "edited_image")

        with col_b:
            file_format = st.selectbox("Format", ["PNG","JPEG"])

        with col_c:
            st.write("")
            st.write("")

            import io
            rgb = cv2.cvtColor(edited_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb)

            buffer = io.BytesIO()
            pil_image.save(buffer, format=file_format)
            byte_img = buffer.getvalue()

            st.download_button(
                "⬇️ Download",
                byte_img,
                file_name=f"{file_name}.{file_format.lower()}",
                mime=f"image/{file_format.lower()}"
            )

    
st.markdown("""
<hr style="opacity:0.2;">
<p style='text-align:center; font-size:14px; opacity:0.7;'>
Made with ❤️ using Streamlit & OpenCV <br>
by Rizwan Hussain
</p>
""", unsafe_allow_html=True)

    




