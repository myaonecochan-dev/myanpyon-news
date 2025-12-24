import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX'; // Replace with USER's actual Measurement ID

export const GoogleAnalytics: React.FC = () => {
    const location = useLocation();
    const isDev = import.meta.env.DEV;

    useEffect(() => {
        if (!isDev) {
            // Production: Inject GA script if not present
            if (!window.gtag) {
                const script = document.createElement('script');
                script.async = true;
                script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
                document.head.appendChild(script);

                window.dataLayer = window.dataLayer || [];
                function gtag(...args: any[]) {
                    window.dataLayer.push(args);
                }
                gtag('js', new Date());
                gtag('config', GA_MEASUREMENT_ID);
                window.gtag = gtag;
            }
        } else {
            console.log(`[Dev:Analytics] Tracker initialized for ${GA_MEASUREMENT_ID}`);
        }
    }, [isDev]);

    useEffect(() => {
        if (!isDev && window.gtag) {
            window.gtag('config', GA_MEASUREMENT_ID, {
                page_path: location.pathname + location.search,
            });
        } else if (isDev) {
            console.log(`[Dev:Analytics] Page View: ${location.pathname}${location.search}`);
        }
    }, [location, isDev]);

    return null; // This component handles side effects only
};

// Add type definition for global gtag
declare global {
    interface Window {
        dataLayer: any[];
        gtag: (...args: any[]) => void;
    }
}
