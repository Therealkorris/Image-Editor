import cv2, os
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFileDialog, QApplication, QCheckBox, QSlider, QComboBox
from PyQt5.QtCore import Qt, QPoint, QThreadPool
from PyQt5.QtGui import QPixmap, QPainter
from ui_components import create_left_panel, create_right_panel
from image_processing import process_image, cv_to_qimage
from ocr_worker import OCRWorker
from ocr_translation import perform_translation
from llava_integration import LlavaWorker

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread_pool = QThreadPool()
        self.image_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.ocr_in_progress = False
        self.llava_analysis_in_progress = False

    def initUI(self):
        self.setWindowTitle('Advanced Image Processor')
        self.setGeometry(100, 100, 1600, 900)

        main_layout = QHBoxLayout()
        
        self.controls = {}
        left_scroll, self.controls, self.image_list, self.upload_btn, self.save_btn, \
        self.auto_ocr_checkbox, self.translate_btn, self.target_lang_combo, self.selection_mode_combo, self.llava_btn = create_left_panel(self)

        right_scroll, self.image_frames, self.image_grid, self.results_layout, \
        self.ocr_results, self.translation_results, self.llava_results = create_right_panel()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_scroll)
        splitter.addWidget(right_scroll)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        self.images = []
        self.current_images = []
        self.processed_images = []
        self.current_image_paths = []
        self.ocr_workers = []
        self.translation_workers = []
        self.llava_workers = []

        # Set initial visibility
        self.set_initial_translation_visibility(False)
        self.toggle_ocr_controls(True)
        self.toggle_color_balance_controls(False)
        self.toggle_llava_controls(False)

    def upload_images(self):
        file_dialog = QFileDialog()
        image_paths, _ = file_dialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if image_paths:
            self.images = []  # Clear existing images
            self.current_image_paths = []  # Clear existing paths
            for path in image_paths:
                img = cv2.imread(path)
                if img is not None:
                    self.images.append(img)
                    self.current_image_paths.append(path)
                    self.image_list.addItem(os.path.basename(path))

            self.update_images()
        else:
            print("No images selected")

    # Make sure this method is correctly updating current_image_paths
    def on_selection_changed(self):
        selected_items = self.image_list.selectedItems()
        selected_indices = [self.image_list.row(item) for item in selected_items]

        self.current_images = [self.images[i] for i in selected_indices if i < len(self.images)]
        self.current_image_paths = [self.current_image_paths[i] for i in selected_indices if i < len(self.current_image_paths)]

        if self.auto_ocr_checkbox.isChecked():
            self.perform_ocr()
        self.update_images()

    def adjust_window_size(self):
        if len(self.images) == 0:
            return

        screen = QApplication.primaryScreen().geometry()
        max_width = int(screen.width() * 0.8)
        max_height = int(screen.height() * 0.8)

        image_width = max(img.shape[1] for img in self.images)
        image_height = max(img.shape[0] for img in self.images)

        total_width = min(image_width * len(self.images), max_width)
        total_height = min(image_height + 400, max_height)  # 400 for controls and results

        self.resize(int(total_width), int(total_height))


    def update_images(self):
        self.processed_images = [process_image(img, self.controls) for img in self.images]
        
        for i, frame in enumerate(self.image_frames):
            if i < len(self.processed_images):
                frame.set_image(self.processed_images[i])
            else:
                frame.set_image(None)

        # Clear previous results
        for ocr_result, translation_result, llava_result in zip(self.ocr_results, self.translation_results, self.llava_results):
            for result in ocr_result + translation_result:
                result.clear()
            llava_result.clear()

        if self.auto_ocr_checkbox.isChecked():
            self.perform_ocr()

        # Force update
        for frame in self.image_frames:
            frame.update()

        self.adjust_window_size()

    def save_image(self):
        if self.processed_images:
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
            if save_path:
                cv2.imwrite(save_path, self.processed_images[0])

    def start_selection(self, event, img_idx):
        if event.button() == Qt.LeftButton:
            self.selecting = True
            self.start_point = self.map_to_image_coordinates(event.pos(), img_idx)

    def update_selection(self, event, img_idx):
        if self.selecting:
            end_point = self.map_to_image_coordinates(event.pos(), img_idx)
            self.draw_selection(img_idx, self.start_point, end_point)

    def end_selection(self, event, img_idx):
        if event.button() == Qt.LeftButton and self.selecting:
            self.selecting = False
            end_point = self.map_to_image_coordinates(event.pos(), img_idx)
            self.selected_areas[img_idx].append((self.start_point, end_point))
            self.draw_selection(img_idx, self.start_point, end_point)

    def map_to_image_coordinates(self, point, img_idx):
        label = self.image_frames[img_idx]
        pixmap = label.pixmap()
        if pixmap is None:
            return point

        label_size = label.size()
        image_rect = pixmap.rect()
        image_rect.moveCenter(label.rect().center())

        # Calculate the scaling factor
        scale_x = self.processed_images[img_idx].shape[1] / image_rect.width()
        scale_y = self.processed_images[img_idx].shape[0] / image_rect.height()

        # Map the point to image coordinates
        x = (point.x() - image_rect.left()) * scale_x
        y = (point.y() - image_rect.top()) * scale_y

        return QPoint(int(x), int(y))

    def set_selection_mode(self, mode):
        for frame in self.image_frames:
            frame.set_selection_mode(mode)

    def draw_selection(self, img_idx, start_point, end_point):
        if img_idx < len(self.processed_images):
            img = self.processed_images[img_idx].copy()
            height, width = img.shape[:2]
            
            # Ensure the points are within the image boundaries
            start_point = QPoint(max(0, min(start_point.x(), width-1)), max(0, min(start_point.y(), height-1)))
            end_point = QPoint(max(0, min(end_point.x(), width-1)), max(0, min(end_point.y(), height-1)))

            # Create a transparent overlay
            overlay = img.copy()
            
            if self.selection_mode == 'rectangle':
                cv2.rectangle(overlay, (start_point.x(), start_point.y()), (end_point.x(), end_point.y()), (0, 255, 0), 2)
            elif self.selection_mode == 'triangle':
                points = np.array([
                    [start_point.x(), start_point.y()],
                    [end_point.x(), start_point.y()],
                    [end_point.x(), end_point.y()]
                ], np.int32)
                cv2.polylines(overlay, [points], True, (0, 255, 0), 2)

            # Blend the overlay with the original image
            alpha = 0.4  # Transparency factor
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            qimg = cv_to_qimage(img)
            pixmap = QPixmap.fromImage(qimg)
            
            label = self.image_frames[img_idx]
            
            # Scale the pixmap to fit the label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Center the pixmap in the label
            x = (label.width() - scaled_pixmap.width()) // 2
            y = (label.height() - scaled_pixmap.height()) // 2
            
            # Create a new pixmap with the label's size and fill it with a background color
            background = QPixmap(label.size())
            background.fill(Qt.white)  # You can change the background color here
            
            # Paint the scaled image onto the background
            painter = QPainter(background)
            painter.drawPixmap(x, y, scaled_pixmap)
            painter.end()
            
            label.setPixmap(background)

            # Store the selection coordinates
            self.selections[img_idx].append((start_point, end_point))

    def perform_ocr(self):
        if self.ocr_in_progress:
            #print("OCR already in progress, skipping...")
            return
        self.ocr_in_progress = True
        #print("Starting perform_ocr method")
        
        if not self.processed_images:
            print("No processed images available")
            self.ocr_in_progress = False
            return

        for ocr_result in self.ocr_results:
            for result in ocr_result:
                result.clear()

        self.ocr_workers.clear()

        for i, img in enumerate(self.processed_images):
            selections = self.image_frames[i].get_selections()
            if selections:
                print(f"Found {len(selections)} selections for image {i}")
                for selection in selections:
                    start, end = selection[0], selection[-1]
                    x1, y1 = min(start.x(), end.x()), min(start.y(), end.y())
                    x2, y2 = max(start.x(), end.x()), max(start.y(), end.y())
                    cropped_img = img[y1:y2, x1:x2]
                    if cropped_img.size > 0:
                        print(f"Processing selection: ({x1}, {y1}) to ({x2}, {y2})")
                        for ocr_type in ['EasyOCR', 'Tesseract']:
                            worker = OCRWorker(cropped_img, ocr_type)
                            worker.finished.connect(lambda text, ocr_type, idx=i: self.update_ocr_result(text, ocr_type, idx))
                            worker.start()
                            self.ocr_workers.append(worker)
            else:
                print(f"No selections for image {i}, using full image")
                for ocr_type in ['EasyOCR', 'Tesseract']:
                    worker = OCRWorker(img, ocr_type)
                    worker.finished.connect(lambda text, ocr_type, idx=i: self.update_ocr_result(text, ocr_type, idx))
                    worker.start()
                    self.ocr_workers.append(worker)

        if not self.ocr_workers:
            print("No OCR workers created")
            for i in range(len(self.processed_images)):
                self.update_ocr_result("No text detected", "EasyOCR", i)
                self.update_ocr_result("No text detected", "Tesseract", i)

        self.ocr_in_progress = False

    def toggle_control_group(self, group_key, state):
        if group_key in self.controls:
            self.controls[group_key].setVisible(state == Qt.Checked)
        
        if group_key == 'ocr_group':
            for i in range(3):
                ocr_group = self.results_layout.itemAtPosition(0, i).widget()
                if ocr_group:
                    ocr_group.setVisible(state == Qt.Checked)
                # Keep translation hidden initially
                translation_group = self.results_layout.itemAtPosition(1, i).widget()
                if translation_group:
                    translation_group.setVisible(False)
        elif group_key == 'llava_group':
            for i in range(3):
                llava_group = self.results_layout.itemAtPosition(2, i).widget()
                if llava_group:
                    llava_group.setVisible(state == Qt.Checked)

    def toggle_translation_visibility(self):
        for i in range(3):
            translation_group = self.results_layout.itemAtPosition(1, i).widget()
            translation_group.setVisible(not translation_group.isVisible())

    def update_ocr_result(self, text, ocr_type, image_index):
        print(f"Updating OCR result for image {image_index}, {ocr_type}")
        print(f"OCR Text: {text[:100]}...")  # Print first 100 characters of the OCR text
        if image_index < len(self.ocr_results):
            if ocr_type == 'EasyOCR':
                self.ocr_results[image_index][0].setPlainText(text)
                print(f"Updated EasyOCR result for image {image_index}")
            elif ocr_type == 'Tesseract':
                self.ocr_results[image_index][1].setPlainText(text)
                print(f"Updated Tesseract result for image {image_index}")
        else:
            print(f"Error: Invalid image index {image_index}")
        
        # Force update of the GUI
        QApplication.processEvents()

    def set_initial_translation_visibility(self, visible=False):
        for i in range(3):
            translation_group = self.results_layout.itemAtPosition(1, i).widget()
            translation_group.setVisible(visible)

    def reset_controls(self):
        for name, control in self.controls.items():
            if isinstance(control, QSlider):
                control.setValue(control.minimum() + (control.maximum() - control.minimum()) // 2)
            elif isinstance(control, QCheckBox):
                control.setChecked(False)
        self.controls['Rotation'].setCurrentIndex(0)
        self.controls['Flip'].setCurrentIndex(0)
        self.update_images()

    def perform_translation(self):
        perform_translation(self)

    def update_translation_result(self, text, status, image_index, ocr_index):
        if status == 'success':
            self.translation_results[image_index][ocr_index].setPlainText(text)
        else:
            self.translation_results[image_index][ocr_index].setPlainText(f"Translation error: {text}")

    def toggle_ocr_controls(self, state):
        self.controls['ocr_group'].setVisible(state)

    def toggle_color_balance_controls(self, state):
        self.controls['color_balance_group'].setVisible(state)

    def toggle_rotation_flip_controls(self, group, button):
        is_visible = group.isVisible()
        group.setVisible(not is_visible)
        button.setText("Hide Rotation and Flip" if not is_visible else "Show Rotation and Flip")

    def toggle_llava_controls(self, state):
        self.controls['llava_group'].setVisible(state)

    def perform_llava_analysis(self):
        if self.llava_analysis_in_progress:
            print("Llava Analysis already in progress, skipping...")
            return

        self.llava_analysis_in_progress = True
        print("Perform Llava Analysis button clicked")

        if not self.processed_images:
            print("No processed images available for Llava analysis")
            self.llava_analysis_in_progress = False
            return

        for llava_result in self.llava_results:
            llava_result.clear()

        self.llava_workers = []  # Clear previous workers

        for i, img in enumerate(self.processed_images):
            print(f"Processing image {i}, shape: {img.shape}")
            selections = self.image_frames[i].get_selections()
            if selections:
                print(f"Found {len(selections)} selections for image {i}")
                for selection in selections:
                    start, end = selection[0], selection[-1]
                    x1, y1 = min(start.x(), end.x()), min(start.y(), end.y())
                    x2, y2 = max(start.x(), end.x()), max(start.y(), end.y())
                    cropped_img = img[y1:y2, x1:x2]
                    if cropped_img.size > 0:
                        print(f"Processing selection: ({x1}, {y1}) to ({x2}, {y2})")
                        worker = LlavaWorker(cropped_img, i)
                        worker.signals.result.connect(self.update_llava_result)
                        self.llava_workers.append(worker)
                        self.thread_pool.start(worker)
            else:
                print(f"No selections for image {i}, using full image")
                worker = LlavaWorker(img, i)
                worker.signals.result.connect(self.update_llava_result)
                self.llava_workers.append(worker)
                self.thread_pool.start(worker)

        print(f"Started {len(self.llava_workers)} Llava analysis workers")
        self.llava_analysis_in_progress = False


    def update_llava_result(self, result, image_index):
        print(f"Received Llava result for image {image_index}")
        if image_index < len(self.llava_results):
            self.llava_results[image_index].setPlainText(result)
            print(f"Updated Llava result for image {image_index}")
        else:
            print(f"Error: Invalid image index {image_index}")

        # Force update of the GUI
        QApplication.processEvents()