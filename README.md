This application serves as an AI-powered bridge between professional networking and personal branding. It uses Gemini 3 Flash (a multimodal LLM) to handle two main workflows:

1. Smart Event Filtering (The "Curator")
The AI acts as a Tech Career Mentor to help you decide if an event is worth your time.

Multimodal Input: It processes both text descriptions and image-based event posters simultaneously.

Skill Extraction: It automatically identifies technical skills (e.g., Python, Cloud Computing, React) mentioned in the invitation.

Worthiness Score: Based on the organizer's type and the event content, it generates a 1-10 score and a logic-based Verdict (e.g., "Must Attend" or "Skip").

2. Automated Brand Building (The "Ghostwriter")
Attending events is only half the battle; the AI helps you share your journey on LinkedIn with zero friction.

Reflection Transformation: You provide raw, messy notes about what you liked or learned at an event.

Professional Formatting: The AI converts those notes into a high-engagement LinkedIn post.

Visibility Optimization: It automatically appends three relevant hashtags to ensure the post reaches the right professional audience.

Technical Workflow
Input: User sends a multipart form containing text and/or an image.

Processing: FastAPI passes the data to the GeminiService which constructs a specialized prompt.

Analysis: The Gemini 3 Flash model performs OCR (Optical Character Recognition) on the image and reasoning on the text.

Output: The system returns a structured JSON response, making it perfect for integration with web or mobile frontends.