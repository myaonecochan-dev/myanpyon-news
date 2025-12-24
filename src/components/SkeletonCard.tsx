import './SkeletonCard.css';

export const SkeletonCard = () => {
    return (
        <div className="skeleton-card">
            <div className="skeleton-thumbnail">
                <div className="skeleton-shimmer"></div>
            </div>
            <div className="skeleton-content">
                <div className="skeleton-title">
                    <div className="skeleton-shimmer"></div>
                </div>
                <div className="skeleton-meta">
                    <div className="skeleton-shimmer"></div>
                </div>
            </div>
        </div>
    );
};
