const StatCard = ({ title, value, subtitle }) => {
    return (
        <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <p className="text-sm text-gray-400">
                {title}
            </p>

            <h2 className="text-3xl font-bold mt-2">
                {value}
            </h2>

            {subtitle && (
                <p className="text-xs text-gray-500 mt-2">
                    {subtitle}
                </p>
            )}
        </div>
    );
};

export default StatCard;