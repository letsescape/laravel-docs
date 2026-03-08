import React, {useState, type ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';
import {codeExamples} from './data';

export default function CodeExamples(): ReactNode {
  const [activeTab, setActiveTab] = useState(codeExamples[0].id);

  const activeExample = codeExamples.find(example => example.id === activeTab);

  return (
    <section className={styles.codeExamples}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <span className={styles.sectionLabel}>백엔드</span>
          <h2 className={styles.sectionTitle}>코드가 스스로 말합니다</h2>
          <p className={styles.sectionDescription}>
            간결하고 우아한 문법이 놀라운 기능을 제공합니다. 모든 기능은 사용자를 배려한 일관된 개발 경험을 제공하기 위해 신중하게 고려되었습니다.
          </p>
        </div>

        <div className={styles.codeExamplesContainer}>
          <div className={styles.tabs}>
            {codeExamples.map(example => (
              <button
                key={example.id}
                className={clsx(styles.tabButton, activeTab === example.id && styles.activeTab)}
                onClick={() => setActiveTab(example.id)}
              >
                {example.title}
              </button>
            ))}
          </div>

          <div className={styles.codeContent}>
            <h3 className={styles.codeTitle}>{activeExample.title}</h3>
            <p className={styles.codeDescription}>{activeExample.description}</p>

            {activeExample.code.map((codeBlock, idx) => (
              <div key={idx} className={styles.codeBlock}>
                <div className={styles.codeHeader}>
                  <span className={styles.codeNumber}>{idx + 1}</span>
                  <span className={styles.codeBlockTitle}>{codeBlock.title}</span>
                </div>
                <pre className={styles.pre}>
                  <code className={styles.code}>
                    {codeBlock.code}
                  </code>
                </pre>
              </div>
            ))}

            <Link to={activeExample.link.url} className={styles.docsLink}>
              {activeExample.link.text}
              <span className={styles.linkArrow}>→</span>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
