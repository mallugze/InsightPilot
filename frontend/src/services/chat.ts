/**
 * AI Assistant Chat API Service Contract for InsightPilot
 * Target Backend: FastAPI
 */

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface SendMessageRequest {
  message: string;
  sessionId: string;
  workspaceId?: string;
}

export interface SendMessageResponse {
  message: ChatMessage;
  success: boolean;
}

/**
 * Sends a query about the active dataset to the AI assistant.
 * @endpoint POST /api/v1/chat/message
 * @headers X-Session-ID
 */
export const sendChatMessage = async (
  data: SendMessageRequest
): Promise<SendMessageResponse> => {
  console.log('[API Request] POST /api/v1/chat/message', data);

  // Simulated AI response delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  return {
    success: true,
    message: {
      id: `msg_${Math.random().toString(36).substr(2, 9)}`,
      sender: 'assistant',
      content: `I analyzed your dataset regarding "${data.message}". Q3 results show a significant correlation between direct sales calls and retail purchase volume. EMEA growth is steady at +12% YoY.`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  };
};
