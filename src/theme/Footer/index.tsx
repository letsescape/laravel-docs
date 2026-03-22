import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

const navColumns = [
  {
    title: 'Products',
    links: [
      {label: 'Cloud', href: 'https://cloud.laravel.com'},
      {label: 'Forge', href: 'https://forge.laravel.com'},
      {label: 'Nightwatch', href: 'https://nightwatch.laravel.com'},
      {label: 'Vapor', href: 'https://vapor.laravel.com'},
      {label: 'Nova', href: 'https://nova.laravel.com'},
    ],
  },
  {
    title: 'Packages',
    links: [
      {label: 'Cashier', href: '/docs/12.x/billing'},
      {label: 'Dusk', href: '/docs/12.x/dusk'},
      {label: 'Horizon', href: '/docs/12.x/horizon'},
      {label: 'Octane', href: '/docs/12.x/octane'},
      {label: 'Scout', href: '/docs/12.x/scout'},
      {label: 'Pennant', href: '/docs/12.x/pennant'},
      {label: 'Pint', href: '/docs/12.x/pint'},
      {label: 'Sail', href: '/docs/12.x/sail'},
      {label: 'Sanctum', href: '/docs/12.x/sanctum'},
      {label: 'Socialite', href: '/docs/12.x/socialite'},
      {label: 'Telescope', href: '/docs/12.x/telescope'},
      {label: 'Pulse', href: '/docs/12.x/pulse'},
      {label: 'Reverb', href: '/docs/12.x/reverb'},
      {label: 'Echo', href: '/docs/12.x/broadcasting'},
    ],
  },
  {
    title: 'Resources',
    links: [
      {label: 'Documentation', href: '/docs/12.x'},
      {label: 'Starter Kits', href: 'https://laravel.com/starter-kits'},
      {label: 'Release Notes', href: '/docs/12.x/releases'},
      {label: 'Blog', href: 'https://blog.laravel.com'},
      {label: 'News', href: 'https://laravel-news.com'},
      {label: 'Community', href: 'https://laravel.com/community'},
      {label: 'Larabelles', href: 'https://larabelles.com/'},
      {label: 'Learn', href: 'https://laravel.com/learn'},
      {label: 'Jobs', href: 'https://larajobs.com/?partner=5'},
      {label: 'Careers', href: 'https://laravel.com/careers'},
      {label: 'Trust', href: 'https://trust.laravel.com'},
    ],
  },
  {
    title: 'Partners',
    links: [
      {label: 'Steadfast Collective', href: 'https://laravel.com/partners/steadfast-collective'},
      {label: 'Redberry', href: 'https://laravel.com/partners/redberry'},
      {label: 'Vehikl', href: 'https://laravel.com/partners/vehikl'},
      {label: 'Swoo', href: 'https://laravel.com/partners/swoo'},
      {label: 'Kirschbaum', href: 'https://laravel.com/partners/kirschbaum'},
      {label: 'Bacancy', href: 'https://laravel.com/partners/bacancy'},
      {label: 'Jump24', href: 'https://laravel.com/partners/jump24'},
      {label: 'CACI Limited', href: 'https://laravel.com/partners/caci-limited'},
      {label: 'Curotec', href: 'https://laravel.com/partners/curotec'},
      {label: '64 Robots', href: 'https://laravel.com/partners/64-robots'},
      {label: 'See All', href: 'https://laravel.com/partners'},
    ],
  },
];

function LaravelLogo(): ReactNode {
  return (
    <svg width="42" height="42" viewBox="0 0 50 52" className="laravel-icon">
      <path d="M49.626 11.564a.809.809 0 0 1 .028.209v10.972a.8.8 0 0 1-.402.694l-9.209 5.302V39.25c0 .286-.152.55-.4.694L20.42 51.01c-.044.025-.092.041-.14.058-.018.006-.035.017-.054.022a.805.805 0 0 1-.41 0c-.022-.006-.042-.018-.063-.026-.044-.016-.09-.03-.132-.054L.402 39.944A.801.801 0 0 1 0 39.25V6.334c0-.072.01-.142.028-.21.006-.023.02-.044.028-.067.015-.042.029-.085.051-.124.015-.026.037-.047.055-.071.023-.032.044-.065.071-.093.023-.023.053-.04.079-.06.029-.024.055-.05.088-.069h.001l9.61-5.533a.802.802 0 0 1 .8 0l9.61 5.533h.002c.032.02.059.045.088.068.026.02.055.038.078.06.028.029.048.062.072.094.017.024.04.045.054.071.023.04.036.082.052.124.008.023.022.044.028.068a.809.809 0 0 1 .028.209v20.559l8.008-4.611v-10.51c0-.07.01-.141.028-.208.007-.024.02-.045.028-.068.016-.042.03-.085.052-.124.015-.026.037-.047.054-.071.024-.032.044-.065.072-.093.023-.023.052-.04.078-.06.03-.024.056-.05.088-.069h.001l9.611-5.533a.801.801 0 0 1 .8 0l9.61 5.533c.034.02.06.045.09.068.025.02.054.038.077.06.028.029.048.062.072.094.018.024.04.045.054.071.023.039.036.082.052.124.009.023.022.044.028.068zm-1.574 10.718v-9.124l-3.363 1.936-4.646 2.675v9.124l8.01-4.611zm-9.61 16.505v-9.13l-4.57 2.61-13.05 7.448v9.216l17.62-10.144zM1.602 7.719v31.068L19.22 48.93v-9.214l-9.204-5.209-.003-.002-.004-.002c-.031-.018-.057-.044-.086-.066-.025-.02-.054-.036-.076-.058l-.002-.003c-.026-.025-.044-.056-.066-.084-.02-.027-.044-.05-.06-.078l-.001-.003c-.018-.03-.029-.066-.042-.1-.013-.03-.03-.058-.038-.09v-.001c-.01-.038-.012-.078-.016-.117-.004-.03-.012-.06-.012-.09v-.002-21.481L4.965 9.654 1.602 7.72zm8.81-5.994L2.405 6.334l8.005 4.609 8.006-4.61-8.006-4.608zm4.164 28.764l4.645-2.674V7.719l-3.363 1.936-4.646 2.675v20.096l3.364-1.937zM39.243 7.164l-8.006 4.609 8.006 4.609 8.005-4.61-8.005-4.608zm-.801 10.605l-4.646-2.675-3.363-1.936v9.124l4.645 2.674 3.364 1.937v-9.124zM20.02 38.33l11.743-6.704 5.87-3.35-8-4.606-9.211 5.303-8.395 4.833 7.993 4.524z" style={{fill: '#f53003'}} fillRule="nonzero"/>
    </svg>
  );
}

function SocialIcons(): ReactNode {
  return (
    <ul className={styles.socialList}>
      <li>
        <a href="https://github.com/laravel" target="_blank" rel="noopener noreferrer" title="GitHub" className={styles.socialLink}>
          <svg className="social-icon" width="24" height="24" viewBox="0 0 24 24" fill="none"><path fillRule="evenodd" clipRule="evenodd" d="M0 12.305C0 17.74 3.438 22.352 8.207 23.979C8.807 24.092 9.027 23.712 9.027 23.386C9.027 23.094 9.016 22.32 9.01 21.293C5.671 22.037 4.967 19.643 4.967 19.643C4.422 18.223 3.635 17.845 3.635 17.845C2.545 17.081 3.718 17.096 3.718 17.096C4.921 17.183 5.555 18.364 5.555 18.364C6.626 20.244 8.364 19.702 9.048 19.386C9.157 18.591 9.468 18.049 9.81 17.741C7.145 17.431 4.344 16.376 4.344 11.661C4.344 10.318 4.811 9.219 5.579 8.359C5.456 8.048 5.044 6.797 5.696 5.103C5.696 5.103 6.704 4.773 8.996 6.364C9.954 6.091 10.98 5.955 12.001 5.95C13.02 5.955 14.047 6.091 15.005 6.364C17.295 4.772 18.302 5.103 18.302 5.103C18.956 6.797 18.544 8.048 18.421 8.359C19.191 9.219 19.655 10.318 19.655 11.661C19.655 16.387 16.849 17.428 14.175 17.732C14.606 18.112 14.99 18.862 14.99 20.011C14.99 21.656 14.975 22.982 14.975 23.386C14.975 23.715 15.191 24.098 15.8 23.977C20.565 22.347 24 17.738 24 12.305C24 5.508 18.627 0 12 0C5.373 0 0 5.508 0 12.305Z" style={{fill: '#737373'}}/></svg>
        </a>
      </li>
      <li>
        <a href="https://x.com/laravelphp" target="_blank" rel="noopener noreferrer" title="X (Twitter)" className={styles.socialLink}>
          <svg className="social-icon" width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M13.969 10.1571L22.7069 0H20.6363L13.0491 8.81931L6.9893 0H0L9.16366 13.3364L0 23.9877H2.07073L10.083 14.6742L16.4826 23.9877H23.4719L13.9684 10.1571H13.969ZM11.1328 13.4538L10.2043 12.1258L2.81684 1.55881H5.99736L11.9592 10.0867L12.8876 11.4147L20.6373 22.4998H17.4567L11.1328 13.4544V13.4538Z" style={{fill: '#737373'}}/></svg>
        </a>
      </li>
      <li>
        <a href="https://www.youtube.com/@LaravelPHP" target="_blank" rel="noopener noreferrer" title="YouTube" className={styles.socialLink}>
          <svg className="social-icon" width="35" height="24" viewBox="0 0 35 24" fill="none"><path d="M33.892 3.75519C33.4994 2.27706 32.3428 1.11294 30.8742 0.717875C28.2124 0 17.5385 0 17.5385 0C17.5385 0 6.8648 0 4.20286 0.717875C2.7343 1.113 1.57768 2.27706 1.18511 3.75519C0.471863 6.43437 0.471863 12.0243 0.471863 12.0243C0.471863 12.0243 0.471863 17.6141 1.18511 20.2933C1.57768 21.7714 2.7343 22.8871 4.20286 23.2821C6.8648 24 17.5385 24 17.5385 24C17.5385 24 28.2123 24 30.8742 23.2821C32.3428 22.8871 33.4994 21.7714 33.892 20.2933C34.6052 17.6141 34.6052 12.0243 34.6052 12.0243C34.6052 12.0243 34.6052 6.43437 33.892 3.75519ZM14.0476 17.0994V6.94906L22.9688 12.0244L14.0476 17.0994Z" style={{fill: '#737373'}}/></svg>
        </a>
      </li>
      <li>
        <a href="https://discord.com/invite/laravel" target="_blank" rel="noopener noreferrer" title="Discord" className={styles.socialLink}>
          <svg className="social-icon" width="33" height="24" viewBox="0 0 33 24" fill="none"><path d="M27.4296 2.00996C25.3491 1.05745 23.1528 0.381713 20.8966 0C20.5879 0.551901 20.3086 1.11973 20.0598 1.70112C17.6566 1.33898 15.2127 1.33898 12.8095 1.70112C12.5605 1.11979 12.2812 0.551968 11.9726 0C9.71504 0.384937 7.51722 1.06228 5.43462 2.01494C1.30013 8.132 0.179328 14.0971 0.739727 19.9776C3.16099 21.7665 5.87108 23.127 8.75218 24C9.40092 23.1275 9.97497 22.2018 10.4682 21.2329C9.53134 20.883 8.62706 20.4512 7.76588 19.9427C7.99253 19.7783 8.2142 19.609 8.42839 19.4446C10.9342 20.623 13.6692 21.234 16.4384 21.234C19.2075 21.234 21.9425 20.623 24.4483 19.4446C24.665 19.6214 24.8867 19.7908 25.1108 19.9427C24.248 20.4521 23.3421 20.8846 22.4035 21.2354C22.8962 22.2039 23.4702 23.1287 24.1196 24C27.0031 23.1305 29.7153 21.7707 32.137 19.9801C32.7945 13.1606 31.0137 7.25031 27.4296 2.00996ZM11.1781 16.3611C9.61644 16.3611 8.32628 14.944 8.32628 13.2005C8.32628 11.457 9.57161 10.0274 11.1731 10.0274C12.7746 10.0274 14.0548 11.457 14.0274 13.2005C14 14.944 12.7696 16.3611 11.1781 16.3611ZM21.6986 16.3611C20.1345 16.3611 18.8493 14.944 18.8493 13.2005C18.8493 11.457 20.0946 10.0274 21.6986 10.0274C23.3026 10.0274 24.5729 11.457 24.5455 13.2005C24.5181 14.944 23.2902 16.3611 21.6986 16.3611Z" style={{fill: '#737373'}}/></svg>
        </a>
      </li>
    </ul>
  );
}

function Footer(): ReactNode {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerInner}>
        <div className={styles.footerMain}>
          {/* Left: branding */}
          <div className={styles.footerBrand}>
            <div className={styles.footerLogo}>
              <LaravelLogo />
            </div>
            <p className={styles.footerTagline}>
              Laravel is the most productive way to build, deploy, and monitor software.
            </p>
            <SocialIcons />
            <div className={styles.footerCopyright}>
              <ul className={styles.copyrightList}>
                <li className={styles.copyrightText}>&copy; 2026 Laravel</li>
                <li><a href="https://laravel.com/legal" className={styles.copyrightLink}>Legal</a></li>
                <li><a href="https://status.laravel.com/" className={styles.copyrightLink}>Status</a></li>
              </ul>
            </div>
          </div>

          {/* Right: nav columns */}
          <div className={styles.footerNav}>
            {navColumns.map((col) => (
              <div key={col.title} className={styles.footerNavCol}>
                <h4 className={styles.footerNavTitle}>{col.title}</h4>
                <ul className={styles.footerNavList}>
                  {col.links.map((link) => (
                    <li key={link.label}>
                      <Link href={link.href} className={styles.footerNavLink}>
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Large Laravel wordmark */}
        <div className={styles.footerWordmark}>
          <img src="/img/title_large.svg" alt="" className={styles.footerWordmarkSvg} />
        </div>
      </div>
    </footer>
  );
}

export default React.memo(Footer);
