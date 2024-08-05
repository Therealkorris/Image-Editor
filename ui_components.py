from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QListWidget,
                             QComboBox, QCheckBox, QGroupBox, QTextEdit, QWidget, QScrollArea, 
                             QSizePolicy, QGridLayout, QTabWidget)
from PyQt5.QtCore import Qt
from image_frame import ImageFrame

def create_control(control_type, name, min_val=None, max_val=None, default_val=None):
    if control_type == 'slider':
        control = QSlider(Qt.Horizontal)
        control.setRange(min_val, max_val)
        control.setValue(default_val)
    elif control_type == 'checkbox':
        control = QCheckBox(name)
        if default_val is None:
            default_val = False  # Ensure default_val is boolean
        control.setChecked(default_val)
    return control

def create_left_panel(parent):
    left_panel = QVBoxLayout()
    controls = {}

    # File operations
    file_group = QGroupBox("File Operations")
    file_layout = QVBoxLayout()
    upload_btn = QPushButton('Upload Images')
    upload_btn.clicked.connect(parent.upload_images)
    file_layout.addWidget(upload_btn)

    image_list = QListWidget()
    image_list.setSelectionMode(QListWidget.ExtendedSelection)
    image_list.itemSelectionChanged.connect(parent.on_selection_changed)
    file_layout.addWidget(image_list)

    save_btn = QPushButton('Save Image')
    save_btn.clicked.connect(parent.save_image)
    file_layout.addWidget(save_btn)
    file_group.setLayout(file_layout)
    left_panel.addWidget(file_group)

    # Control visibility
    visibility_group = QGroupBox("Show/Hide Controls")
    visibility_layout = QVBoxLayout()
    
    control_groups = [
        ("Image Processing", "processing_group"),
        ("Color Balance", "color_balance_group"),
        ("Rotation and Flip", "rotation_flip_group"),
        ("OCR and Translation", "ocr_group"),
        ("Llava Analysis", "llava_group")
    ]
    
    visibility_checkboxes = {}
    for group_name, group_key in control_groups:
        checkbox = QCheckBox(f"Show {group_name} Controls")
        checkbox.setChecked(False)
        visibility_checkboxes[group_key] = checkbox
        visibility_layout.addWidget(checkbox)
    
    visibility_group.setLayout(visibility_layout)
    left_panel.addWidget(visibility_group)
    
    # Create all control groups
    processing_group = create_processing_controls(parent, controls)
    color_balance_group = create_color_balance_controls(parent, controls)
    rotation_flip_group = create_rotation_flip_controls(parent, controls)
    ocr_group, auto_ocr_checkbox, translate_btn, target_lang_combo, selection_mode_combo = create_ocr_controls(parent, controls)
    llava_group, llava_btn = create_llava_controls(parent, controls)

    # Add control groups to layout and set initial visibility
    for group, group_key in [
        (processing_group, "processing_group"),
        (color_balance_group, "color_balance_group"),
        (rotation_flip_group, "rotation_flip_group"),
        (ocr_group, "ocr_group"),
        (llava_group, "llava_group")
    ]:
        left_panel.addWidget(group)
        group.setVisible(False)
        controls[group_key] = group
        visibility_checkboxes[group_key].stateChanged.connect(
            lambda state, key=group_key: parent.toggle_control_group(key, state)
        )

    reset_btn = QPushButton('Reset to Default')
    reset_btn.clicked.connect(parent.reset_controls)
    left_panel.addWidget(reset_btn)

    left_scroll = QScrollArea()
    left_widget = QWidget()
    left_widget.setLayout(left_panel)
    left_scroll.setWidget(left_widget)
    left_scroll.setWidgetResizable(True)
    left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    return left_scroll, controls, image_list, upload_btn, save_btn, auto_ocr_checkbox, translate_btn, target_lang_combo, selection_mode_combo, llava_btn

def create_right_panel():
    right_panel = QVBoxLayout()

    # Image display
    image_grid = QGridLayout()
    image_frames = []
    
    # Create image frames for 3 images
    for i in range(3):
        frame = ImageFrame()
        image_frames.append(frame)
        image_grid.addWidget(frame, 0, i)

    image_widget = QWidget()
    image_widget.setLayout(image_grid)
    image_scroll_area = QScrollArea()
    image_scroll_area.setWidget(image_widget)
    image_scroll_area.setWidgetResizable(True)
    right_panel.addWidget(image_scroll_area)

    # Results display
    results_tab_widget = QTabWidget()
    results_layout = QGridLayout()
    ocr_results = []
    translation_results = []
    llava_results = []

    # Create result widgets for 3 images
    for i in range(3):
        # OCR results
        ocr_group = QGroupBox(f"Image {i+1} OCR Results")
        ocr_group.setVisible(False)  # Initially hidden
        ocr_layout = QVBoxLayout()
        easyocr_result = QTextEdit()
        easyocr_result.setReadOnly(True)
        ocr_layout.addWidget(QLabel("EasyOCR"))
        ocr_layout.addWidget(easyocr_result)
        tesseract_result = QTextEdit()
        tesseract_result.setReadOnly(True)
        ocr_layout.addWidget(QLabel("Tesseract"))
        ocr_layout.addWidget(tesseract_result)
        ocr_group.setLayout(ocr_layout)
        results_layout.addWidget(ocr_group, 0, i)
        ocr_results.append((easyocr_result, tesseract_result))

        # Translation results
        translation_group = QGroupBox(f"Image {i+1} Translation Results")
        translation_group.setVisible(False)
        translation_layout = QVBoxLayout()  
        easyocr_translation = QTextEdit()
        easyocr_translation.setReadOnly(True)
        translation_layout.addWidget(QLabel("EasyOCR Translation"))
        translation_layout.addWidget(easyocr_translation)
        tesseract_translation = QTextEdit()
        tesseract_translation.setReadOnly(True)
        translation_layout.addWidget(QLabel("Tesseract Translation"))
        translation_layout.addWidget(tesseract_translation)
        translation_group.setLayout(translation_layout)
        results_layout.addWidget(translation_group, 1, i)
        translation_results.append((easyocr_translation, tesseract_translation))


        # Llava results
        llava_group = QGroupBox(f"Image {i+1} Llava Analysis")
        llava_group.setVisible(False)  # Initially hidden
        llava_layout = QVBoxLayout()
        llava_result = QTextEdit()
        llava_result.setReadOnly(True)
        llava_layout.addWidget(llava_result)
        llava_group.setLayout(llava_layout)
        results_layout.addWidget(llava_group, 2, i)
        llava_results.append(llava_result)

    results_widget = QWidget()
    results_widget.setLayout(results_layout)
    results_scroll = QScrollArea()
    results_scroll.setWidget(results_widget)
    results_scroll.setWidgetResizable(True)
    results_tab_widget.addTab(results_scroll, "Results")

    right_panel.addWidget(results_tab_widget)

    right_scroll = QScrollArea()
    right_widget = QWidget()
    right_widget.setLayout(right_panel)
    right_scroll.setWidget(right_widget)
    right_scroll.setWidgetResizable(True)

    return right_scroll, image_frames, image_grid, results_layout, ocr_results, translation_results, llava_results

def create_processing_controls(parent, controls):
    processing_group = QGroupBox("Image Processing")
    processing_layout = QVBoxLayout()
    control_params = [
        ('Brightness', 'slider', -100, 100, 0),
        ('Contrast', 'slider', -100, 100, 0),
        ('Saturation', 'slider', -100, 100, 0),
        ('Hue', 'slider', -180, 180, 0),
        ('Gamma', 'slider', 1, 50, 10),
        ('Blur', 'slider', 0, 20, 0),
        ('Sharpen', 'slider', 0, 10, 0),
        ('Noise', 'slider', 0, 50, 0),
        ('Edge Detection', 'slider', 0, 100, 0),
        ('Greyscale', 'checkbox', False),
        ('Invert', 'checkbox', False),
        ('Sepia', 'checkbox', False),
    ]

    for name, control_type, *params in control_params:
        control = create_control(control_type, name, *params)
        controls[name] = control
        processing_layout.addWidget(QLabel(name))
        processing_layout.addWidget(control)
        if control_type == 'slider':
            control.valueChanged.connect(parent.update_images)
            control.sliderMoved.connect(lambda value, s=control: s.setToolTip(str(value)))
        elif control_type == 'checkbox':
            control.stateChanged.connect(parent.update_images)

    processing_group.setLayout(processing_layout)
    return processing_group

def create_color_balance_controls(parent, controls):
    color_balance_group = QGroupBox("Color Balance")
    color_balance_layout = QVBoxLayout()
    for color in ['Red', 'Green', 'Blue']:
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-100)
        slider.setMaximum(100)
        slider.setValue(0)
        slider.valueChanged.connect(parent.update_images)
        slider.sliderMoved.connect(lambda value, s=slider: s.setToolTip(str(value)))
        color_balance_layout.addWidget(QLabel(color))
        color_balance_layout.addWidget(slider)
        controls[f'Color Balance {color}'] = slider
    color_balance_group.setLayout(color_balance_layout)
    return color_balance_group

def create_rotation_flip_controls(parent, controls):
    rotation_flip_group = QGroupBox("Rotation and Flip")
    rotation_flip_layout = QVBoxLayout()
    rotation_combo = QComboBox()
    rotation_combo.addItems(['No Rotation', 'Rotate 90°', 'Rotate 180°', 'Rotate 270°'])
    rotation_combo.currentIndexChanged.connect(parent.update_images)
    rotation_flip_layout.addWidget(QLabel("Rotation"))
    rotation_flip_layout.addWidget(rotation_combo)
    controls['Rotation'] = rotation_combo

    flip_combo = QComboBox()
    flip_combo.addItems(['No Flip', 'Flip Horizontal', 'Flip Vertical'])
    flip_combo.currentIndexChanged.connect(parent.update_images)
    rotation_flip_layout.addWidget(QLabel("Flip"))
    rotation_flip_layout.addWidget(flip_combo)
    controls['Flip'] = flip_combo

    rotation_flip_group.setLayout(rotation_flip_layout)
    return rotation_flip_group

def create_ocr_controls(parent, controls):
    ocr_group = QGroupBox("OCR and Translation")
    ocr_layout = QVBoxLayout()
    ocr_group.setVisible(False)
    
    ocr_btn = QPushButton('Perform OCR')
    ocr_btn.clicked.connect(parent.perform_ocr)
    ocr_layout.addWidget(ocr_btn)

    auto_ocr_checkbox = QCheckBox("Auto OCR")
    auto_ocr_checkbox.setChecked(False)
    ocr_layout.addWidget(auto_ocr_checkbox)

    translate_btn = QPushButton('Show/Hide Translation')
    translate_btn.clicked.connect(parent.toggle_translation_visibility)
    ocr_layout.addWidget(translate_btn)

    target_lang_combo = QComboBox()
    target_lang_combo.addItems(['en', 'es', 'fr', 'de', 'it', 'ja', 'ko', 'zh-cn'])
    ocr_layout.addWidget(QLabel("Target Language"))
    ocr_layout.addWidget(target_lang_combo)

    # Add selection mode dropdown
    selection_mode_combo = QComboBox()
    selection_mode_combo.addItems(['Rectangle', 'Triangle'])
    selection_mode_combo.currentTextChanged.connect(lambda text: parent.set_selection_mode(text.lower()))
    ocr_layout.addWidget(QLabel("Selection Mode"))
    ocr_layout.addWidget(selection_mode_combo)

    ocr_group.setLayout(ocr_layout)
    
    controls['Auto OCR'] = auto_ocr_checkbox
    controls['Translate'] = translate_btn
    controls['Target Language'] = target_lang_combo
    controls['Selection Mode'] = selection_mode_combo
    
    return ocr_group, auto_ocr_checkbox, translate_btn, target_lang_combo, selection_mode_combo
def create_llava_controls(parent, controls):
    llava_group = QGroupBox("Llava Image Analysis")
    llava_layout = QVBoxLayout()
    llava_btn = QPushButton('Perform Llava Analysis')
    llava_btn.clicked.connect(parent.perform_llava_analysis)
    llava_layout.addWidget(llava_btn)
    llava_group.setLayout(llava_layout)
    controls['Llava Analysis'] = llava_btn
    return llava_group, llava_btn