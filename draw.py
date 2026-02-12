import cv2
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import utils as ut



def draw_line(image, color_hex, thickness):

    if "draw_line_key" not in st.session_state:
        st.session_state.draw_line_key = 0

    if "line_start" not in st.session_state:
        st.session_state.line_start = None

    if "last_click" not in st.session_state:
        st.session_state.last_click = None

    if st.session_state.get("draw_mode") != "line":
        return image

    h, w = image.shape[:2]
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    coords = streamlit_image_coordinates(
        pil_img,key=f"draw-line-{st.session_state.draw_line_key}",use_column_width=True)

    if not coords:
        return image

    scale_x = w / coords["width"]
    scale_y = h / coords["height"]

    x = int(coords["x"] * scale_x)
    y = int(coords["y"] * scale_y)
    point = (x, y)


    if st.session_state.last_click == point:
        return image

    st.session_state.last_click = point

    if st.session_state.line_start is None:
        st.session_state.line_start = point
        st.toast("Start point selected 🎯")
        return image

    p1 = st.session_state.line_start
    p2 = point

    color = ut.hex_to_bgr(color_hex)

    scale = (scale_x + scale_y) / 2
    real_thickness = max(1, int(thickness * scale))

    cv2.line(image, p1, p2, color, real_thickness)

    st.session_state.line_start = None
    st.session_state.draw_mode = None
    st.session_state.draw_line_key += 1

    st.toast("Line drawn ✅")

    st.rerun()



def draw_rect(image, color_hex, thickness, filled):

    if "rect_start" not in st.session_state:
        st.session_state.rect_start = None

    if "draw_rect_key" not in st.session_state:
        st.session_state.draw_rect_key = 0

    mode = st.session_state.get("draw_mode")

    if mode not in ["rectangle", "square"]:
        return image


    h, w = image.shape[:2]
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    coords = streamlit_image_coordinates(
        pil_img,
        key=f"draw-rect-{st.session_state.draw_rect_key}",
        use_column_width=True
    )

    if not coords:
        return image


    scale_x = w / coords["width"]
    scale_y = h / coords["height"]

    x = int(coords["x"] * scale_x)
    y = int(coords["y"] * scale_y)
    point = (x, y)

    if st.session_state.rect_start is None:
        st.session_state.rect_start = point
        st.toast("Corner selected 🎯")
        return image

    x1, y1 = st.session_state.rect_start
    x2, y2 = point

    if mode == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        x2 = x1 + side if x2 > x1 else x1 - side
        y2 = y1 + side if y2 > y1 else y1 - side


    color = ut.hex_to_bgr(color_hex)

    scale = (scale_x + scale_y) / 2
    real_thickness = -1 if filled else max(1, int(thickness * scale))

    cv2.rectangle(image, (x1, y1), (x2, y2), color, real_thickness)


    st.session_state.rect_start = None
    st.session_state.draw_mode = None
    st.session_state.draw_rect_key += 1

    st.toast("Shape drawn ✅")

    st.rerun()

    return image

def draw_circle(image,color_hex,thickness,filled,radius):
    if "circle_center" not in st.session_state :
        st.session_state.circle_center = None
    if "draw_circle_key" not in st.session_state:
        st.session_state.draw_circle_key = 0
    if st.session_state.get("draw_mode")!= "circle":
        return image
    
    h,w = image.shape[:2]
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    coords = streamlit_image_coordinates(pil_img, key=f"draw-circle-{st.session_state.draw_circle_key}",use_column_width=True)
    if not coords:
        return image
    
    scale_x = w/coords["width"]
    scale_y = h/coords["height"]

    x = int(coords["x"]*scale_x)
    y = int(coords["y"]*scale_y)

    center = (x,y)
    color = ut.hex_to_bgr(color_hex)

    real_thickness = -1 if filled else thickness
    cv2.circle(image,center,radius,color,real_thickness)

    st.session_state.draw_mode = None
    st.session_state.draw_circle_key += 1
    st.toast("Circle drawn ✅")
    st.rerun()
    return image


def draw_text(image,text,font_name,font_scale,thickness,color_hex):
    if "draw_text_key" not in st.session_state:
        st.session_state.draw_text_key = 0

    if not st.session_state.get("text_mode"):
        return image
    
    font_map = {"Simplex": cv2.FONT_HERSHEY_SIMPLEX,
    "Plain": cv2.FONT_HERSHEY_PLAIN,
    "Duplex": cv2.FONT_HERSHEY_DUPLEX,
    "Complex": cv2.FONT_HERSHEY_COMPLEX,
    "Triplex": cv2.FONT_HERSHEY_TRIPLEX,
    "Complex Small": cv2.FONT_HERSHEY_COMPLEX_SMALL,
    "Script Simplex": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    "Script Complex": cv2.FONT_HERSHEY_SCRIPT_COMPLEX,}

    font = font_map[font_name]
    h,w = image.shape[:2]
    rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    coords = streamlit_image_coordinates(pil_img,key=f"draw-text-{st.session_state.draw_text_key}",use_column_width=True)
    if not coords:
        return image
    
    scale_x = w/coords["width"]
    scale_y = h/coords["height"]

    x =int(coords["x"]*scale_x)
    y =int(coords["y"]*scale_y)

    color = ut.hex_to_bgr(color_hex)

    cv2.putText(image,text,(x,y),font,font_scale,color,thickness,cv2.LINE_AA)
    st.session_state.text_mode = False
    st.session_state.draw_text_key += 1
    st.toast("Text added ✅")
    st.rerun()
    return image