export function LoadingState() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
      <div className="flex flex-col items-center justify-center py-6">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
        <h3 className="text-lg font-medium text-gray-900 mb-1">Verifying claim against official records...</h3>
        <p className="text-sm text-gray-500">Checking Electoral Commission data</p>
      </div>
    </div>
  );
}
