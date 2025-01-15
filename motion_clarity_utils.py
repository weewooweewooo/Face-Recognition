import cv2
import numpy as np
import collections
import logging


class MotionClarityUtils:
    def __init__(
        self, frame_size=(300, 300), motion_threshold=5.0, clarity_threshold=30
    ):
        self.frame_size = frame_size
        self.previous_frame = None
        self.frame_buffer = collections.deque(maxlen=5)
        self.motion_scores = collections.deque(maxlen=5)
        self.frame_clarity_scores = collections.deque(maxlen=5)
        self.motion_threshold = motion_threshold
        self.clarity_threshold = clarity_threshold
        self.motion_tolerance = 50.0
        self.motion_weight = 0.5
        self.high_motion_count = 0
        self.low_clarity_count = 0
        self.min_clarity_to_skip_blur = 20

    def update_thresholds(self):
        if self.motion_scores:
            avg_motion = np.mean(self.motion_scores)
            self.motion_threshold = max(3.0, min(7.0, avg_motion * 1.2))

        if self.clarity_threshold:
            avg_clarity = np.mean(self.clarity_threshold)
            self.clarity_threshold = max(30.0, min(70.0, avg_clarity * 0.8))

    def measure_clarity(self, image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            laplacian_var = min(laplacian_var, 150.0)

            self.frame_clarity_scores.append(laplacian_var)

            smoothed_clarity = np.median(self.frame_clarity_scores)
            self.update_thresholds()

            avg_motion = np.mean(self.motion_scores) if self.motion_scores else 0.0
            adjusted_clarity_threshold = (
                self.clarity_threshold * 0.8
                if avg_motion > self.motion_threshold * 0.5
                else self.clarity_threshold
            )

            if smoothed_clarity < adjusted_clarity_threshold:
                logging.info("Low clarity detected.")
                return False, smoothed_clarity

            return True, smoothed_clarity
        except Exception as e:
            logging.error(f"Error measuring clarity: {e}")
            return False, 0.0

    def smooth_motion_scores(self, alpha=0.2):
        smoothed_scores = []
        for i, score in enumerate(self.motion_scores):
            if i == 0:
                smoothed_scores.append(score)
            else:
                smoothed_scores.append(
                    alpha * score + (1 - alpha) * smoothed_scores[-1]
                )
        return smoothed_scores[-1]

    def check_motion(self, frame, bbox=None):
        try:
            if bbox:
                x1, y1, x2, y2 = map(int, bbox)
                frame_resized = cv2.resize(frame[y1:y2, x1:x2], self.frame_size)
            else:
                frame_resized = cv2.resize(frame, self.frame_size)

            if self.previous_frame is None:
                self.previous_frame = frame_resized
                self.motion_scores.append(0.0)
                return True

            prev_gray = cv2.cvtColor(self.previous_frame, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
            prev_gray = cv2.GaussianBlur(prev_gray, (5, 5), 0)
            curr_gray = cv2.GaussianBlur(curr_gray, (5, 5), 0)
            diff = cv2.absdiff(prev_gray, curr_gray)
            motion_score = np.mean(diff)
            self.previous_frame = frame_resized

            # Append motion score and update thresholds
            self.motion_scores.append(motion_score)
            self.update_thresholds()

            avg_motion = self.smooth_motion_scores()
            smoothed_motion_score = np.mean(self.motion_scores)

            # Adjusted threshold with more tolerance
            adjusted_threshold = max(self.motion_threshold * 0.7, 2.0)

            if smoothed_motion_score < adjusted_threshold:
                self.high_motion_count += 1
                if (
                    self.high_motion_count >= 3
                ):  # Require 3 consecutive low-motion frames
                    logging.info("Low motion detected; likely static image.")
                    return False
            else:
                self.high_motion_count = 0

            return True
        except Exception as e:
            logging.error(f"Error in motion detection: {e}")
            self.previous_frame = None
            return True

    def check_clarity(self, face_crop):
        try:
            clarity_valid, clarity_score = self.measure_clarity(face_crop)
            if not clarity_valid:
                if clarity_score > self.min_clarity_to_skip_blur:
                    logging.info(
                        f"Clarity Score: {clarity_score:.2f}, Threshold: {self.clarity_threshold:.2f}"
                    )
                    logging.info("Skipping blurred frame during motion.")
                    return False, None
                logging.info("Frame clarity too low.")
                return False, False
            return True, True
        except Exception as e:
            logging.error(f"Error in check_clarity: {e}")
            return False, False

    def analyze_texture(self, face_crop):
        try:
            gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()  # Measure texture

            texture_threshold_min = 50.0
            texture_threshold_max = 1000.0
            logging.info(f"Texture Score: {laplacian_var:.2f}")

            if (
                laplacian_var < texture_threshold_min
                or laplacian_var > texture_threshold_max
            ):
                logging.info("Low texture detected: Likely a photo.")
                return False
            return True
        except Exception as e:
            logging.error(f"Error in texture analysis: {e}")
            return False

    def analyze_frequency(self, face_crop):
        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = 20 * np.log(np.abs(f_shift))
        
        mean_frequency = np.mean(magnitude_spectrum)
        logging.info(f"Mean Frequency: {mean_frequency:.2f}")
        frequency_threshold = 100.0
        if mean_frequency < frequency_threshold:
            logging.info("Low frequency detected: Likely a photo.")
            return False
        return True

    def detect_head_movement(self, previous_landmarks, current_landmarks):
        movement_threshold = 10
        movement = np.linalg.norm(
            np.array(current_landmarks) - np.array(previous_landmarks)
        )
        if movement < movement_threshold:
            logging.info(f"Insufficient head movement: {movement:.2f}. Likely a photo.")
            return False
        return True
