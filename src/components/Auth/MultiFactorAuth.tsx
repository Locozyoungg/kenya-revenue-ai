/**
 * MFA Component for taxpayer and KRA staff login
 * Supports SMS (via Safaricom API) and Email verification
 */
const MultiFactorAuth = () => {
    const [step, setStep] = useState<'init' | 'verify'>('init');
    const [phone, setPhone] = useState('');
  
    const sendOTP = async () => {
      await fetch('/api/auth/send-otp', {
        method: 'POST',
        body: JSON.stringify({ phone }),
      });
      setStep('verify');
    };
  
    return (
      <div className="max-w-md mx-auto p-4">
        {step === 'init' ? (
          <>
            <input
              type="tel"
              placeholder="07XX XXX XXX"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="border p-2 w-full mb-4"
            />
            <button 
              onClick={sendOTP}
              className="bg-blue-600 text-white p-2 w-full rounded"
            >
              {t('sendOtp')}
            </button>
          </>
        ) : (
          <OTPVerification 
            phone={phone}
            onSuccess={() => redirectToDashboard()}
          />
        )}
      </div>
    );
  };