/**
 * Mobile-first dashboard for taxpayers (Swahili/English)
 * Features:
 * - Tax filing status
 * - Payment history
 * - AI-generated compliance tips
 */
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { MpesaPaymentButton } from '../../components/Payment';

const TaxpayerDashboard = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<'status' | 'history'>('status');

  // Mock data from backend API
  const taxStatus = {
    pin: 'A001234567M',
    balance: 15000,
    dueDate: '2024-06-30',
    complianceScore: 82,
  };

  return (
    <div className="container mx-auto p-4">
      {/* Language Toggle */}
      <div className="flex justify-end mb-4">
        <button 
          onClick={() => i18n.changeLanguage('sw')}
          className="mr-2 text-blue-600"
        >
          Swahili
        </button>
        <button 
          onClick={() => i18n.changeLanguage('en')}
          className="text-blue-600"
        >
          English
        </button>
      </div>

      {/* Tax PIN and Balance */}
      <div className="bg-white rounded-lg p-4 shadow-md mb-4">
        <h2 className="text-xl font-bold mb-2">
          {t('welcome')}, {taxStatus.pin}
        </h2>
        <p className="text-gray-600">
          {t('balance')}: KES {taxStatus.balance.toLocaleString()}
        </p>
        <p className="text-red-500">
          {t('dueDate')}: {taxStatus.dueDate}
        </p>
      </div>

      {/* Compliance Tips from AI */}
      <div className="bg-blue-50 p-4 rounded-lg mb-4">
        <h3 className="font-bold mb-2">{t('complianceTips')}</h3>
        <p>
          {t('aiSuggestion')}: {taxStatus.complianceScore}% {t('complianceScore')}
        </p>
      </div>

      {/* Payment Button */}
      <MpesaPaymentButton 
        amount={taxStatus.balance}
        onSuccess={() => alert(t('paymentSuccess'))}
      />
    </div>
  );
};