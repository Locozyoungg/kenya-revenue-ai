/**
 * KRA Admin Dashboard with real-time revenue analytics
 * Integrates with backend fraud detection API
 */
import { FraudsChart, RevenueMap } from '../../components/Analytics';

const AdminDashboard = () => {
  // Fetch data from backend API
  const analyticsData = useFraudAnalytics();
  const { t } = useTranslation();

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">{t('kraDashboard')}</h1>
      
      {/* Real-Time Revenue Map */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <RevenueMap 
          data={analyticsData.regional}
          title={t('revenueByCounty')}
        />
      </div>

      {/* Fraud Detection Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <FraudsChart 
          detected={analyticsData.fraudsDetected}
          resolved={analyticsData.fraudsResolved}
        />
        <ComplianceChart 
          scores={analyticsData.complianceScores}
        />
      </div>

      {/* High-Risk Taxpayers Table */}
      <RiskTable 
        taxpayers={analyticsData.highRisk}
        onAudit={(pin) => handleAudit(pin)}
      />
    </div>
  );
};