import React, {type ReactNode} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

const products = [
  {name: 'Cloud', url: 'https://cloud.laravel.com'},
  {name: 'Forge', url: 'https://forge.laravel.com'},
  {name: 'Nightwatch', url: 'https://nightwatch.laravel.com'},
  {name: 'Vapor', url: 'https://vapor.laravel.com'},
  {name: 'Nova', url: 'https://nova.laravel.com'},
];

const packages = [
  {name: 'Cashier', url: '/docs/billing'},
  {name: 'Dusk', url: '/docs/dusk'},
  {name: 'Horizon', url: '/docs/horizon'},
  {name: 'Octane', url: '/docs/octane'},
  {name: 'Scout', url: '/docs/scout'},
  {name: 'Pennant', url: '/docs/pennant'},
  {name: 'Pint', url: '/docs/pint'},
  {name: 'Sail', url: '/docs/sail'},
  {name: 'Sanctum', url: '/docs/sanctum'},
  {name: 'Socialite', url: '/docs/socialite'},
  {name: 'Telescope', url: '/docs/telescope'},
  {name: 'Pulse', url: '/docs/pulse'},
  {name: 'Reverb', url: '/docs/reverb'},
  {name: 'Echo', url: '/docs/broadcasting'},
];

const resources = [
  {name: 'Documentation', url: '/docs'},
  {name: 'Starter Kits', url: '/starter-kits'},
  {name: 'Release Notes', url: '/docs/releases'},
  {name: 'Blog', url: 'https://blog.laravel.com'},
  {name: 'News', url: 'https://laravel-news.com'},
  {name: 'Community', url: '/community'},
  {name: 'Larabelles', url: 'https://www.larabelles.com'},
  {name: 'Learn', url: 'https://bootcamp.laravel.com'},
  {name: 'Jobs', url: 'https://larajobs.com'},
  {name: 'Careers', url: '/careers'},
  {name: 'Trust', url: 'https://trust.laravel.com'},
];

const partners = [
  {name: 'Threadable', url: '/partners/threadable'},
  {name: 'Vehikl', url: '/partners/vehikl'},
  {name: 'Redberry', url: '/partners/redberry'},
  {name: 'CACI Limited', url: '/partners/caci-limited'},
  {name: 'Steadfast Collective', url: '/partners/steadfast-collective'},
  {name: 'byte5', url: '/partners/byte5'},
  {name: 'UCodeSoft', url: '/partners/ucodesoft'},
  {name: 'Kirschbaum', url: '/partners/kirschbaum'},
  {name: 'Pixel', url: '/partners/pixel'},
  {name: 'Jump24', url: '/partners/jump24'},
  {name: 'See All', url: '/partners'},
];

export default function FooterSection(): ReactNode {
  const legalUrl = useBaseUrl('/legal');
  const wordmarkUrl = useBaseUrl('/img/title_large.svg');
  return (
    <footer className="hp-footer">
      <div className="container">
        <div className="footer-top">
          {/* Brand column */}
          <div className="footer-brand">
            <svg viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg" className="footer-logo-icon">
              <path d="M49.626 11.564a.809.809 0 0 1 .028.209v10.972a.8.8 0 0 1-.402.694l-9.209 5.302V39.25c0 .286-.152.55-.4.694L20.42 51.01c-.044.025-.092.041-.14.058-.018.006-.035.017-.054.022a.805.805 0 0 1-.41 0c-.022-.006-.042-.018-.063-.026-.044-.016-.09-.03-.132-.054L.402 39.944A.801.801 0 0 1 0 39.25V6.334c0-.072.01-.142.028-.21.006-.023.02-.044.028-.067.015-.042.029-.085.051-.124.015-.026.037-.047.055-.071.023-.032.044-.065.071-.093.023-.023.053-.04.079-.06.029-.024.055-.05.088-.069h.001l9.61-5.533a.802.802 0 0 1 .8 0l9.61 5.533h.002c.032.02.059.045.088.068.026.02.055.038.078.06.028.029.048.062.072.094.017.024.04.045.054.071.023.04.036.082.052.124.008.023.022.044.028.068a.809.809 0 0 1 .028.209v20.559l8.008-4.611v-10.51c0-.07.01-.141.028-.208.007-.024.02-.045.028-.068.016-.042.03-.085.052-.124.015-.026.037-.047.054-.071.024-.032.044-.065.072-.093.023-.023.052-.04.078-.06.03-.024.056-.05.088-.069h.001l9.611-5.533a.801.801 0 0 1 .8 0l9.61 5.533c.034.02.06.045.09.068.025.02.054.038.077.06.028.029.048.062.072.094.018.024.04.045.054.071.023.039.036.082.052.124.009.023.022.044.028.068zm-1.574 10.718v-9.124l-3.363 1.936-4.646 2.675v9.124l8.01-4.611zm-9.61 16.505v-9.13l-4.57 2.61-13.05 7.448v9.216l17.62-10.144zM1.602 7.719v31.068L19.22 48.93v-9.214l-9.204-5.209-.003-.002-.004-.002c-.031-.018-.057-.044-.086-.066-.025-.02-.054-.036-.076-.058l-.002-.003c-.026-.025-.044-.056-.066-.084-.02-.027-.044-.05-.06-.078l-.001-.003c-.018-.03-.029-.066-.042-.1-.013-.03-.03-.058-.038-.09v-.001c-.01-.038-.012-.078-.016-.117-.004-.03-.012-.06-.012-.09v-.002-21.481L4.965 9.654 1.602 7.72zm8.81-5.994L2.405 6.334l8.005 4.609 8.006-4.61-8.006-4.608zm4.164 28.764l4.645-2.674V7.719l-3.363 1.936-4.646 2.675v20.096l3.364-1.937zM39.243 7.164l-8.006 4.609 8.006 4.609 8.005-4.61-8.005-4.608zm-.801 10.605l-4.646-2.675-3.363-1.936v9.124l4.645 2.674 3.364 1.937v-9.124zM20.02 38.33l11.743-6.704 5.87-3.35-8-4.606-9.211 5.303-8.395 4.833 7.993 4.524z" fill="currentColor" />
            </svg>
            <p>
              Laravel is the most productive way to{' '}
              <span className="footer-brand-br" />
              build, deploy, and monitor software.
            </p>
            <div className="footer-social footer-social-icons">
              <a
                href="https://github.com/laravel"
                aria-label="Laravel on GitHub"
                target="_blank"
                rel="noopener noreferrer"
              >
                <svg width="32" height="32" viewBox="0 0 24 24" className="footer-social-svg">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                </svg>
              </a>
              <a
                href="https://x.com/laravelphp"
                aria-label="Laravel on X"
                target="_blank"
                rel="noopener noreferrer"
              >
                <svg width="28" height="28" viewBox="0 0 24 24" className="footer-social-svg">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
              </a>
              <a
                href="https://www.youtube.com/@LaravelPHP"
                aria-label="Laravel on YouTube"
                target="_blank"
                rel="noopener noreferrer"
              >
                <svg width="32" height="32" viewBox="0 0 24 24" className="footer-social-svg">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
                </svg>
              </a>
              <a
                href="https://discord.com/invite/laravel"
                aria-label="Laravel on Discord"
                target="_blank"
                rel="noopener noreferrer"
              >
                <svg width="32" height="32" viewBox="0 0 24 24" className="footer-social-svg">
                  <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561 19.9187 19.9187 0 005.9933 3.0294.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286 19.8674 19.8674 0 006.0023-3.0294.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189z" fillRule="evenodd" />
                </svg>
              </a>
            </div>
            <div className="footer-brand-bottom">
              <span>&copy; 2026 Laravel</span>
              <a href={legalUrl}>Legal</a>
              <a href="https://status.laravel.com/" target="_blank" rel="noopener noreferrer">Status</a>
            </div>
          </div>

          <div className="footer-columns-right">
            {/* Products column */}
            <div className="footer-column">
              <h4>Products</h4>
              <ul>
                {products.map(item => (
                  <li key={item.name}>
                    <a href={item.url} target="_blank" rel="noopener noreferrer">
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Packages column */}
            <div className="footer-column">
              <h4>Packages</h4>
              <ul>
                {packages.map(item => (
                  <li key={item.name}>
                    <a href={item.url}>{item.name}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Resources column */}
            <div className="footer-column">
              <h4>Resources</h4>
              <ul>
                {resources.map(item => (
                  <li key={item.name}>
                    <a
                      href={item.url}
                      {...(item.url.startsWith('http') ? {target: '_blank', rel: 'noopener noreferrer'} : {})}
                    >
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Partners column */}
            <div className="footer-column">
              <h4>Partners</h4>
              <ul>
                {partners.map(item => (
                  <li key={item.name}>
                    <a href={item.url}>{item.name}</a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Laravel wordmark */}
        <div className="footer-wordmark">
          <img
            src={wordmarkUrl}
            alt="Laravel"
            className="footer-wordmark-img"
          />
        </div>
      </div>
    </footer>
  );
}
