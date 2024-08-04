from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QImage, QPolygon
import cv2

class ImageFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.pixmap = None
        self.scaled_pixmap = None
        self.selections = []
        self.current_selection = None
        self.setMinimumSize(400, 400)
        self.selection_mode = 'rectangle'  # Default selection mode

    def set_image(self, image):
        self.image = image
        if self.image is not None:
            height, width, channel = self.image.shape
            bytes_per_line = 3 * width
            q_image = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.pixmap = QPixmap.fromImage(q_image)
        else:
            self.pixmap = None
        self.update_scaled_pixmap()
        self.update()

    def update_scaled_pixmap(self):
        if self.pixmap:
            margin_percent = 0.00  # 5% margin
            available_width = int(self.width() * (1 - 2 * margin_percent))
            available_height = int(self.height() * (1 - 2 * margin_percent))
            self.scaled_pixmap = self.pixmap.scaled(available_width, available_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            self.scaled_pixmap = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  # Fill background with white

        if self.scaled_pixmap:
            # Calculate position to center the image
            x = (self.width() - self.scaled_pixmap.width()) // 2
            y = (self.height() - self.scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, self.scaled_pixmap)

            # Draw selections
            painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
            for selection in self.selections:
                self.draw_selection(painter, selection)
            
            if self.current_selection:
                self.draw_selection(painter, self.current_selection)

    def set_selection_mode(self, mode):
        self.selection_mode = mode
        self.update()

    def draw_selection(self, painter, selection):
        if len(selection) < 2:
            return

        start = self.map_from_image_coordinates(selection[0])
        end = self.map_from_image_coordinates(selection[-1])

        if self.selection_mode == 'rectangle':
            painter.drawRect(QRect(start, end))
        elif self.selection_mode == 'triangle':
            points = QPolygon([
                start,
                QPoint(end.x(), start.y()),
                end
            ])
            painter.drawPolygon(points)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_scaled_pixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_selection = [self.map_to_image_coordinates(event.pos())]
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.current_selection:
            self.current_selection.append(self.map_to_image_coordinates(event.pos()))
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_selection:
            self.selections.append([p for p in self.current_selection if p is not None])
            self.current_selection = None
            self.update()
            self.selection_changed.emit()

    def map_to_image_coordinates(self, point):
        if not self.scaled_pixmap:
            return None
        
        x = (self.width() - self.scaled_pixmap.width()) // 2
        y = (self.height() - self.scaled_pixmap.height()) // 2
        pixmap_rect = QRect(x, y, self.scaled_pixmap.width(), self.scaled_pixmap.height())
        
        if not pixmap_rect.contains(point):
            return None
        
        x_ratio = self.pixmap.width() / pixmap_rect.width()
        y_ratio = self.pixmap.height() / pixmap_rect.height()
        
        x = (point.x() - pixmap_rect.left()) * x_ratio
        y = (point.y() - pixmap_rect.top()) * y_ratio
        
        return QPoint(int(x), int(y))

    def map_from_image_coordinates(self, point):
        if not self.scaled_pixmap or point is None:
            return QPoint()
        
        x = (self.width() - self.scaled_pixmap.width()) // 2
        y = (self.height() - self.scaled_pixmap.height()) // 2
        pixmap_rect = QRect(x, y, self.scaled_pixmap.width(), self.scaled_pixmap.height())
        
        x_ratio = pixmap_rect.width() / self.pixmap.width()
        y_ratio = pixmap_rect.height() / self.pixmap.height()
        
        x = point.x() * x_ratio + pixmap_rect.left()
        y = point.y() * y_ratio + pixmap_rect.top()
        
        return QPoint(int(x), int(y))

    def get_selections(self):
        return self.selections

    def clear_selections(self):
        self.selections.clear()
        self.update()