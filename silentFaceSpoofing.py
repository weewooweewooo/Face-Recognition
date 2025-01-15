import torch
import logging
from torchvision import transforms
from model import MiniFASNetV2  # Assuming the model class is defined in model.py

class SilentFaceAntiSpoofing:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        # Load the MiniFASNetV2 model
        state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
        
        # Remove 'module.' prefix if present
        new_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('module.'):
                new_state_dict[k[7:]] = v
            else:
                new_state_dict[k] = v
        
        model = MiniFASNetV2(conv6_kernel=(5, 5)).to(self.device)  # Initialize the model architecture with the correct kernel size
        model.load_state_dict(new_state_dict)
        model.eval()
        return model

    def preprocess(self, face_crop):
        # Preprocess the face_crop for the model
        transform = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize((80, 80)),  # Update to the correct input size
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5], std=[0.5]),
            ]
        )
        return transform(face_crop).unsqueeze(0).to(self.device)

    def predict(self, face_crop):
        try:
            input_tensor = self.preprocess(face_crop)
            with torch.no_grad():
                output = self.model(input_tensor)
                prediction = torch.sigmoid(output).squeeze()  # Handle multi-element tensor
                # Assuming the model outputs a multi-class prediction, take the maximum value
                prediction = prediction.max().item()
                return prediction > 0.5  # Adjust threshold as needed
        except Exception as e:
            logging.error(f"Error in anti-spoofing prediction: {e}")
            return False
