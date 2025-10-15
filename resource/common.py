
window_width = 600
window_height = 400

profile_w = int(window_width*0.28)
profile_h = 50
profile_x = int(window_width*0.73) # RIGHT
profile_y = 2


toolbar_w = int(window_width*0.98)
toolbar_h = int(window_height*0.2)
toolbar_x = int((window_width-toolbar_w)/2) # CENTERED
toolbar_y = int(window_height*0.0625)

table_w = int(window_width*0.95)
table_h = int(window_height*0.7)
table_x = int((window_width-table_w)/2) # CENTERED
table_y = int((window_height*0.2))

overlay_w = int(window_width*0.30)
overlay_h = int(window_height*0.45)
overlay_x = int((window_width-overlay_w)/2) # CENTERED
overlay_y = int(window_height*0.15)

statusbar_w = window_width
statusbar_h = 25
statusbar_x = 0
statusbar_y = int(window_height-statusbar_h)





# STYLES
main_styles = """
    QLabel#title {font-size: 28px; font-weight: bold; margin-left: 5px;}
"""
overlay_styles = """
    QFrame {background-color: rgba(0, 0, 0, 0.9); border-radius: 10px; padding-top: 10px}
"""


# FUNCTION
def validate_number(value) -> int | float:
    try:
        number = float(value)
        return int(number) if number.is_integer() else number
    except (ValueError, TypeError):
        return 0