import React, {type ReactNode} from 'react';
import styles from './styles.module.css';

interface Event {
  name: string;
  dates: string;
  location: string;
  color: string;
}

const events: Event[] = [
  {name: 'Laravel Live Japan', dates: 'May 26-27, 2026', location: 'Tokyo', color: 'linear-gradient(135deg, #e73c3c, #c0392b)'},
  {name: 'Laravel Live UK', dates: 'Jun 18-19, 2026', location: 'London', color: 'linear-gradient(135deg, #3498db, #2980b9)'},
  {name: 'Laracon US', dates: 'Jul 28-29, 2026', location: 'Boston', color: 'linear-gradient(135deg, #e67e22, #d35400)'},
  {name: 'Laravel Live Denmark', dates: 'Aug 20-21, 2026', location: 'Copenhagen', color: 'linear-gradient(135deg, #2ecc71, #27ae60)'},
];

export default function EventsSection(): ReactNode {
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <p className={styles.sectionLabel}>이벤트</p>
          <h2 className={styles.sectionTitle}>도쿄에서 만나요</h2>
          <p className={styles.sectionDescription}>
            전 세계에서 열리는 Laravel 커뮤니티 이벤트에 참여하세요.
          </p>
        </div>

        <div className={styles.eventsGrid}>
          {events.map((event, idx) => (
            <div key={idx} className={styles.eventCard}>
              <div className={styles.eventImage} style={{background: event.color}}>
                {event.name}
              </div>
              <div className={styles.eventBody}>
                <h3 className={styles.eventName}>{event.name}</h3>
                <p className={styles.eventMeta}>
                  {event.dates}
                  <br />
                  {event.location}
                </p>
                <a href="#" className={styles.eventLink}>
                  티켓 확보하기 →
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
