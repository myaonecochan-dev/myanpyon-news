import './FloatingDonationButton.css';

export const FloatingDonationButton: React.FC = () => {
    return (
        <a
            href="https://ko-fi.com/nyanpyon"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Support on Ko-fi"
            className="donation-button"
        >
            <span role="img" aria-label="cat-can" className="donation-icon">🥫</span>
            <span className="donation-text">猫缶を贈る</span>
        </a>
    );
};
