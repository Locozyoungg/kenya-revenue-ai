/**
 * Mobile-friendly tax filing form with Swahili support
 * Auto-calculates taxes based on M-Pesa transaction data
 */
const MobileTaxForm = () => {
    const { t } = useTranslation();
    const [declarations, setDeclarations] = useState<IncomeDeclaration[]>([]);
  
    // Auto-fill from M-Pesa API
    const autoFillIncome = async () => {
      const mpesaData = await fetchMpesaTransactions();
      setDeclarations(mpesaData.transactions);
    };
  
    return (
      <div className="p-4">
        <h2 className="text-xl font-bold mb-4">{t('fileReturn')}</h2>
        
        {/* Auto-Fill Button */}
        <button 
          onClick={autoFillIncome}
          className="bg-green-600 text-white p-2 rounded mb-4"
        >
          {t('autoFillMpesa')}
        </button>
  
        {/* Income Declaration Table */}
        <table className="w-full">
          <thead>
            <tr>
              <th>{t('month')}</th>
              <th>{t('income')}</th>
              <th>{t('tax')}</th>
            </tr>
          </thead>
          <tbody>
            {declarations.map((declaration) => (
              <tr key={declaration.month}>
                <td>{declaration.month}</td>
                <td>KES {declaration.income.toLocaleString()}</td>
                <td>KES {declaration.tax.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
  
        {/* AI Validation */}
        <AIValidationWarning 
          declarations={declarations}
          onConfirm={() => submitToKRA()}
        />
      </div>
    );
  };