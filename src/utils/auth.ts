export const login = async (phone: string, otp: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ phone, otp }),
    });
    return response.json();
  };
  
  export const logout = () => {
    localStorage.removeItem('authToken');
  };