/**
 * Authentication API Service Contract for InsightPilot
 * Target Backend: FastAPI
 */

export interface RegisterRequest {
  fullName: string;
  email: string;
  companyName?: string;
}

export interface RegisterResponse {
  success: boolean;
  userId: string;
  session_id: string;
  emailVerified: boolean;
  message: string;
}

export interface VerifyRequest {
  code: string;
  session_id: string;
}

export interface VerifyResponse {
  success: boolean;
  isEmailVerified: boolean;
  message: string;
}

/**
 * Registers user profile locally and generates backend payload contract.
 * @endpoint POST /api/v1/auth/register
 */
export const registerUser = async (data: RegisterRequest): Promise<RegisterResponse> => {
  console.log('[API Request] POST /api/v1/auth/register', data);
  
  // Simulated backend delay
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    success: true,
    userId: 'usr_mock_123456',
    session_id: localStorage.getItem('insight_pilot_session_id') || 'session_local_uuid',
    emailVerified: false,
    message: 'Registration successful. Verification code dispatched to email.',
  };
};

/**
 * Submits 6-digit email confirmation code.
 * @endpoint POST /api/v1/auth/verify
 */
export const verifyCode = async (data: VerifyRequest): Promise<VerifyResponse> => {
  console.log('[API Request] POST /api/v1/auth/verify', data);

  // Simulated backend delay
  await new Promise((resolve) => setTimeout(resolve, 600));

  if (data.code.trim().length === 6) {
    return {
      success: true,
      isEmailVerified: true,
      message: 'Email verified successfully.',
    };
  }

  return {
    success: false,
    isEmailVerified: false,
    message: 'Invalid code provided.',
  };
};
