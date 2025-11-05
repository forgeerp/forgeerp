import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { api, Configuration, ConfigurationCreate } from '../lib/api';

export function Configurations() {
  const { t } = useTranslation();
  const [configurations, setConfigurations] = useState<Configuration[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<ConfigurationCreate>({
    key: '',
    value: '',
    value_type: 'string',
    description: null,
  });

  useEffect(() => {
    loadConfigurations();
  }, []);

  const loadConfigurations = async () => {
    try {
      setLoading(true);
      const response = await api.get<{ configurations: Configuration[]; total: number }>(
        '/api/v1/configurations'
      );
      setConfigurations(response.configurations);
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : t('configurations.createError'));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      if (editingId) {
        await api.patch(`/api/v1/configurations/${editingId}`, {
          value: formData.value,
          value_type: formData.value_type,
          description: formData.description,
        });
      } else {
        await api.post('/api/v1/configurations', formData);
      }
      
      await loadConfigurations();
      resetForm();
    } catch (err) {
      setError(err instanceof Error ? err.message : t('configurations.updateError'));
    }
  };

  const handleEdit = (config: Configuration) => {
    setEditingId(config.id);
    setFormData({
      key: config.key,
      value: config.value,
      value_type: config.value_type,
      description: config.description || null,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t('configurations.deleteConfirm'))) {
      return;
    }

    try {
      await api.delete(`/api/v1/configurations/${id}`);
      await loadConfigurations();
    } catch (err) {
      setError(err instanceof Error ? err.message : t('configurations.deleteError'));
    }
  };

  const resetForm = () => {
    setFormData({
      key: '',
      value: '',
      value_type: 'string',
      description: null,
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) {
    return <div className="text-gray-600">{t('common.loading')}</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">{t('configurations.title')}</h2>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + {t('configurations.newConfiguration')}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Form */}
      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {editingId ? t('configurations.editConfiguration') : t('configurations.newConfiguration')}
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('configurations.key')} *
                </label>
                <input
                  type="text"
                  required
                  value={formData.key}
                  onChange={(e) => setFormData({ ...formData, key: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder={t('configurations.key')}
                  disabled={!!editingId}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('configurations.value')} *
                </label>
                <input
                  type="text"
                  required
                  value={formData.value}
                  onChange={(e) => setFormData({ ...formData, value: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder={t('configurations.value')}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('configurations.valueType')}
                </label>
                <select
                  value={formData.value_type}
                  onChange={(e) => setFormData({ ...formData, value_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="string">String</option>
                  <option value="number">Number</option>
                  <option value="boolean">Boolean</option>
                  <option value="json">JSON</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('configurations.description')}
                </label>
                <input
                  type="text"
                  value={formData.description || ''}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value || null })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder={t('configurations.description')}
                />
              </div>
            </div>
            <div className="flex justify-end gap-3">
              <button
                type="button"
                onClick={resetForm}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300"
              >
                {t('common.cancel')}
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {editingId ? t('common.update') : t('common.create')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Configurations List */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">{t('configurations.title')}</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('configurations.key')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('configurations.value')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('configurations.valueType')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('configurations.description')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('common.actions')}
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {configurations.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                    {t('configurations.noConfigurations')}
                  </td>
                </tr>
              ) : (
                configurations.map((config) => (
                  <tr key={config.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {config.key}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {config.value}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {config.value_type}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {config.description || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => handleEdit(config)}
                        className="text-blue-600 hover:text-blue-900 mr-4"
                      >
                        {t('common.edit')}
                      </button>
                      <button
                        onClick={() => handleDelete(config.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        {t('common.delete')}
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
