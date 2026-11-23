
import logging
import cv2
import numpy as np

from hailo_platform import (
    HEF,
    VDevice,
    HailoStreamInterface,
    ConfigureParams,
    InputVStreamParams,
    OutputVStreamParams,
    FormatType,
    InferVStreams
)

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    VEHICLE_CLASSES
)


class VehicleDetector:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Hailo model not found: {MODEL_PATH}"
            )

        self.hef = HEF(str(MODEL_PATH))
        self.device = VDevice()

        params = ConfigureParams.create_from_hef(
            self.hef,
            interface=HailoStreamInterface.PCIe
        )

        self.network_group = self.device.configure(
            self.hef, params
        )[0]

        self.network_params = (
            self.network_group.create_params()
        )

        self.input_info = (
            self.hef.get_input_vstream_infos()[0]
        )

        self.output_infos = (
            self.hef.get_output_vstream_infos()
        )

        self.input_params = (
            InputVStreamParams.make_from_network_group(
                self.network_group,
                quantized=False,
                format_type=FormatType.FLOAT32
            )
        )

        self.output_params = (
            OutputVStreamParams.make_from_network_group(
                self.network_group,
                quantized=False,
                format_type=FormatType.FLOAT32
            )
        )

        self.height, self.width, self.channels = (
            self.input_info.shape
        )

        self.pipeline = None
        self.activation = None

        self._start_pipeline()

        self.logger.info(
            "Hailo detector initialized: %s",
            self.input_info.shape
        )

    def _start_pipeline(self):

        self.activation = self.network_group.activate(
            self.network_params
        )

        self.activation.__enter__()

        self.pipeline = InferVStreams(
            self.network_group,
            self.input_params,
            self.output_params
        )

        self.pipeline.__enter__()

    def preprocess(self, frame):

        resized = cv2.resize(
            frame,
            (self.width, self.height)
        )

        rgb = cv2.cvtColor(
            resized,
            cv2.COLOR_BGR2RGB
        )

        return rgb.astype(np.float32)

    def infer(self, frame):

        prepared = self.preprocess(frame)

        input_data = {
            self.input_info.name:
                np.expand_dims(prepared, axis=0)
        }

        outputs = self.pipeline.infer(input_data)

        return self.postprocess(outputs, frame.shape)

    def postprocess(self, outputs, original_shape):

        original_height, original_width = (
            original_shape[:2]
        )

        detections = []

        for output_name, output in outputs.items():

            if isinstance(output, list):
                output = np.asarray(output)

            output = np.asarray(output)

            # Common Hailo NMS output:
            # one detection array per class.
            if output.dtype == object:
                continue

            if output.ndim >= 3:
                output = output.reshape(-1, output.shape[-1])

            if output.ndim == 2 and output.shape[-1] == 6:

                for row in output:

                    x1, y1, x2, y2, score, class_id = row

                    self._append_detection(
                        detections,
                        x1, y1, x2, y2,
                        score, class_id,
                        original_width,
                        original_height
                    )

        if not detections:
            self.logger.debug(
                "No supported detections decoded. "
                "Check the HEF output format."
            )

        return detections

    def _append_detection(
        self,
        results,
        x1, y1, x2, y2,
        score, class_id,
        frame_width,
        frame_height
    ):

        score = float(score)
        class_id = int(class_id)

        if score < CONFIDENCE_THRESHOLD:
            return

        if class_id not in VEHICLE_CLASSES:
            return

        # Accept normalized or model-pixel coordinates.
        if max(abs(float(x1)), abs(float(x2))) <= 1.5:
            x1 *= frame_width
            x2 *= frame_width
            y1 *= frame_height
            y2 *= frame_height
        else:
            x1 *= frame_width / self.width
            x2 *= frame_width / self.width
            y1 *= frame_height / self.height
            y2 *= frame_height / self.height

        x1 = int(np.clip(x1, 0, frame_width - 1))
        x2 = int(np.clip(x2, 0, frame_width - 1))
        y1 = int(np.clip(y1, 0, frame_height - 1))
        y2 = int(np.clip(y2, 0, frame_height - 1))

        if x2 <= x1 or y2 <= y1:
            return

        results.append({
            "bbox": (x1, y1, x2, y2),
            "confidence": score,
            "class_id": class_id
        })

    def release(self):

        if self.pipeline is not None:
            self.pipeline.__exit__(None, None, None)
            self.pipeline = None

        if self.activation is not None:
            self.activation.__exit__(None, None, None)
            self.activation = None

        if self.device is not None:
            self.device.release()
            self.device = None
