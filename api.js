import axios from "axios";

const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;

export const sendMessageToChatGPT = async (message) => {
  const endpoint = "https://api.openai.com/v1/chat/completions";

  try {
    const response = await axios.post(
      endpoint,
      {
        model: "gpt-3.5-turbo", // Change model if needed
        messages: [{ role: "user", content: message }],
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${API_KEY}`,
        },
      }
    );

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error("Error fetching response:", error);
    return "Error fetching response. Please try again.";
  }
};
