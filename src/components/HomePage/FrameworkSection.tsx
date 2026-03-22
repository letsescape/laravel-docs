import React, {useState, type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './FrameworkSection.module.css';

// Helper to render syntax-highlighted code
function CodeLine({children}: {children: ReactNode}) {
  return <div className={styles.codeLine}>{children}</div>;
}

function K({children}: {children: ReactNode}) {
  return <span className={styles.codeKeyword}>{children}</span>;
}
function F({children}: {children: ReactNode}) {
  return <span className={styles.codeFunction}>{children}</span>;
}
function S({children}: {children: ReactNode}) {
  return <span className={styles.codeString}>{children}</span>;
}
function V({children}: {children: ReactNode}) {
  return <span className={styles.codeVariable}>{children}</span>;
}
function R({children}: {children: ReactNode}) {
  return <span className={styles.codeReturn}>{children}</span>;
}
function C({children}: {children: ReactNode}) {
  return <span className={styles.codeClass}>{children}</span>;
}
function A({children}: {children: ReactNode}) {
  return <span className={styles.codeArrow}>{children}</span>;
}
function T({children}: {children: ReactNode}) {
  return <span className={styles.codeTag}>{children}</span>;
}

const categories = [
  {
    name: 'Auth',
    files: [
      {
        name: 'web.php',
        code: (
          <>
            <CodeLine><C>Route</C>::<F>get</F>(<S>'/dashboard'</S>, <K>function</K> (<C>Request</C> <V>$request</V>) {'{'}</CodeLine>
            <CodeLine>    <V>$user</V> = <V>$request</V><A>⟶</A><F>user</F>();</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>    <R>return</R> <F>view</F>(<S>'dashboard'</S>, [<S>'user'</S> <A>⟹</A> <V>$user</V>]);</CodeLine>
            <CodeLine>{'}'})-&gt;<F>middleware</F>(<S>'auth'</S>);</CodeLine>
          </>
        ),
      },
      {
        name: 'FlightController.php',
        code: (
          <>
            <CodeLine><K>class</K> <C>FlightController</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    #[<F>Middleware</F>(<S>'auth'</S>)]</CodeLine>
            <CodeLine>    #[<F>Authorize</F>(<S>'view'</S>, <S>'flight'</S>)]</CodeLine>
            <CodeLine>    <K>public function</K> <F>show</F>(<C>Flight</C> <V>$flight</V>): <C>View</C></CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <R>return</R> <F>view</F>(<S>'dashboard'</S>, [<S>'user'</S> <A>⟹</A> <V>$user</V>]);</CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'AI SDK',
    files: [
      {
        name: 'api.php',
        code: (
          <>
            <CodeLine><K>use</K> App{'\\'}Ai{'\\'}Agents{'\\'}<C>SalesCoach</C>;</CodeLine>
            <CodeLine><K>use</K> Illuminate{'\\'}Http{'\\'}<C>Request</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine><C>Route</C>::<F>post</F>(<S>'/coach'</S>, <K>function</K> (<C>Request</C> <V>$request</V>) {'{'}</CodeLine>
            <CodeLine>    <V>$response</V> = (<K>new</K> <C>SalesCoach</C>)</CodeLine>
            <CodeLine>        <A>⟶</A><F>prompt</F>(<S>'Analyze this sales transcript...'</S>, attachments: [</CodeLine>
            <CodeLine>            <V>$request</V><A>⟶</A><F>file</F>(<S>'transcript'</S>),</CodeLine>
            <CodeLine>        ]);</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>    <R>return</R> [</CodeLine>
            <CodeLine>        <S>'analysis'</S> <A>⟹</A> (<K>string</K>) <V>$response</V>,</CodeLine>
            <CodeLine>    ];</CodeLine>
            <CodeLine>{'}'});</CodeLine>
          </>
        ),
      },
      {
        name: 'SalesCoach.php',
        code: (
          <>
            <CodeLine><K>namespace</K> <C>AppAiAgents</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine><K>use</K> Laravel{'\\'}Ai{'\\'}<C>ContractsAgent</C>;</CodeLine>
            <CodeLine><K>use</K> Laravel{'\\'}Ai{'\\'}<C>Promptable</C>;</CodeLine>
            <CodeLine><K>use</K> <C>Stringable</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine><K>class</K> <C>SalesCoach</C> <K>implements</K> <C>Agent</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    <K>use</K> <C>Promptable</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>    <span className={styles.codeComment}>{'/**'}</span></CodeLine>
            <CodeLine>    <span className={styles.codeComment}>{' * Get the instructions that the agent should follow.'}</span></CodeLine>
            <CodeLine>    <span className={styles.codeComment}>{' */'}</span></CodeLine>
            <CodeLine>    <K>public function</K> <F>instructions</F>(): <C>Stringable</C>|<K>string</K></CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <R>return</R> <S>'You are a sales coach, analyzing transcripts and providing feedback.'</S>;</CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'ORM',
    files: [
      {
        name: 'Flight.php',
        code: (
          <>
            <CodeLine>  <K>namespace</K> <C>App{'\\'}Models</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>  <K>use</K> Illuminate{'\\'}Database{'\\'}Eloquent{'\\'}<C>Model</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>  <K>class</K> <C>Flight</C> <K>extends</K> <C>Model</C></CodeLine>
            <CodeLine>  {'{'}</CodeLine>
            <CodeLine>      <span className={styles.codeComment}>{'// ...'}</span></CodeLine>
            <CodeLine>  {'}'}</CodeLine>
          </>
        ),
      },
      {
        name: 'web.php',
        code: (
          <>
            <CodeLine><K>use</K> App{'\\'}Models{'\\'}<C>Flight</C>;</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine><R>foreach</R> (<C>Flight</C>::<F>all</F>() as <V>$flight</V>) {'{'}</CodeLine>
            <CodeLine>    <F>echo</F> <V>$flight</V><A>⟶</A>name;</CodeLine>
            <CodeLine>{'}'}</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine><C>Flight</C>::<F>create</F>([</CodeLine>
            <CodeLine>    <S>'name'</S> <A>⟹</A> <S>'New flight'</S>,</CodeLine>
            <CodeLine>]);</CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'Migrations',
    files: [
      {
        name: 'create_posts_table.php',
        code: (
          <>
            <CodeLine><K>class</K> <C>CreatePostsTable</C> <K>extends</K> <C>Migration</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    <K>public function</K> <F>up</F>()</CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <C>Schema</C>::<F>create</F>(<S>'posts'</S>, <K>function</K> (<C>Blueprint</C> <V>$table</V>) {'{'}</CodeLine>
            <CodeLine>            <V>$table</V><A>⟶</A><F>id</F>();</CodeLine>
            <CodeLine>            <V>$table</V><A>⟶</A><F>string</F>(<S>'title'</S>);</CodeLine>
            <CodeLine>            <V>$table</V><A>⟶</A><F>text</F>(<S>'content'</S>);</CodeLine>
            <CodeLine>            <V>$table</V><A>⟶</A><F>foreignId</F>(<S>'user_id'</S>)<A>⟶</A><F>constrained</F>()<A>⟶</A><F>onDelete</F>(<S>'cascade'</S>);</CodeLine>
            <CodeLine>            <V>$table</V><A>⟶</A><F>timestamps</F>();</CodeLine>
            <CodeLine>        {'}'});</CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'Validation',
    files: [
      {
        name: 'PostController.php',
        code: (
          <>
            <CodeLine><K>class</K> <C>PostController</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    <K>public function</K> <F>store</F>(<C>Request</C> <V>$request</V>)</CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <V>$validated</V> = <V>$request</V><A>⟶</A><F>validate</F>([</CodeLine>
            <CodeLine>            <S>'title'</S> <A>⟹</A> <S>'required|max:255'</S>,</CodeLine>
            <CodeLine>            <S>'content'</S> <A>⟹</A> <S>'required'</S>,</CodeLine>
            <CodeLine>        ]);</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>        <span className={styles.codeComment}>{'// ...'}</span></CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
      {
        name: 'post.blade.php',
        code: (
          <>
            <CodeLine><K>@if</K> (<V>$errors</V><A>⟶</A><F>any</F>())</CodeLine>
            <CodeLine>    <T>&lt;div</T> <span style={{color: '#E50000'}}>class</span>=<K>"alert alert-danger"</K><T>&gt;</T></CodeLine>
            <CodeLine>        <T>&lt;ul&gt;</T></CodeLine>
            <CodeLine>            <K>@foreach</K> (<V>$errors</V><A>⟶</A><F>all</F>() as <V>$error</V>)</CodeLine>
            <CodeLine>                <T>&lt;li&gt;</T><F>{'{{ '}</F><V>$error</V><F>{' }}'}</F><T>&lt;/li&gt;</T></CodeLine>
            <CodeLine>            <K>@endforeach</K></CodeLine>
            <CodeLine>        <T>&lt;/ul&gt;</T></CodeLine>
            <CodeLine>    <T>&lt;/div&gt;</T></CodeLine>
            <CodeLine><K>@endif</K></CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'Storage',
    files: [
      {
        name: 'PostController.php',
        code: (
          <>
            <CodeLine><K>class</K> <C>PostController</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    <K>public function</K> <F>store</F>(<C>Request</C> <V>$request</V>)</CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <R>if</R> (<V>$request</V><A>⟶</A><F>hasFile</F>(<S>'image'</S>)) {'{'}</CodeLine>
            <CodeLine>            <V>$path</V> = <V>$request</V><A>⟶</A><F>file</F>(<S>'image'</S>)<A>⟶</A><F>store</F>(<S>'images'</S>, <S>'public'</S>);</CodeLine>
            <CodeLine>        {'}'}</CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'Queues',
    files: [
      {
        name: 'ProcessPost.php',
        code: (
          <>
            <CodeLine><K>class</K> <C>ProcessPost</C> <K>implements</K> <C>ShouldQueue</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    <K>public function</K> <F>handle</F>()</CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <K>$this</K><A>⟶</A><V>post</V><A>⟶</A><F>update</F>([</CodeLine>
            <CodeLine>            <S>'rendered_content'</S> <A>⟹</A> <C>Str</C>::<F>markdown</F>(<K>$this</K><A>⟶</A><V>post</V><A>⟶</A><V>content</V>)</CodeLine>
            <CodeLine>        ]);</CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
      {
        name: 'PostController.php',
        code: (
          <>
            <CodeLine><K>class</K> <C>PostController</C></CodeLine>
            <CodeLine>{'{'}</CodeLine>
            <CodeLine>    <K>public function</K> <F>store</F>(<C>Request</C> <V>$request</V>)</CodeLine>
            <CodeLine>    {'{'}</CodeLine>
            <CodeLine>        <V>$post</V> = <C>Post</C>::<F>create</F>(<V>$request</V><A>⟶</A><F>all</F>());</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>        <C>ProcessPost</C>::<F>dispatch</F>(<V>$post</V>);</CodeLine>
            <CodeLine>    {'}'}</CodeLine>
            <CodeLine>{'}'}</CodeLine>
          </>
        ),
      },
    ],
  },
  {
    name: 'Testing',
    files: [
      {
        name: 'BasicTest.php',
        code: (
          <>
            <CodeLine><F>it</F>(<S>'can create a post'</S>, <K>function</K> () {'{'}</CodeLine>
            <CodeLine>    <V>$response</V> = <K>$this</K><A>⟶</A><F>post</F>(<S>'/posts'</S>, [</CodeLine>
            <CodeLine>        <S>'title'</S> <A>⟹</A> <S>'Test Post'</S>,</CodeLine>
            <CodeLine>        <S>'content'</S> <A>⟹</A> <S>'This is a test post content.'</S>,</CodeLine>
            <CodeLine>    ]);</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>    <V>$response</V><A>⟶</A><F>assertStatus</F>(<span style={{color: '#098658'}}>302</span>);</CodeLine>
            <CodeLine>{'\u00A0'}</CodeLine>
            <CodeLine>    <K>$this</K><A>⟶</A><F>assertDatabaseHas</F>(<S>'posts'</S>, [</CodeLine>
            <CodeLine>        <S>'title'</S> <A>⟹</A> <S>'Test Post'</S>,</CodeLine>
            <CodeLine>    ]);</CodeLine>
            <CodeLine>{'}'});</CodeLine>
          </>
        ),
      },
    ],
  },
];

const features = [
  'Starter kits for React, Vue, and Svelte',
  'AI SDK and Boost AI assistant',
  'Database ORM, queues, routing, and more',
  'Open source ecosystem of over 30 packages',
];

export default function FrameworkSection(): ReactNode {
  const [aiEnabled, setAiEnabled] = useState(true);
  const [activeCategory, setActiveCategory] = useState(0);
  const [activeFile, setActiveFile] = useState(0);

  const category = categories[activeCategory];
  const file = category.files[activeFile];

  return (
    <>
      {/* Header */}
      <section className={styles.header}>
        <div className={styles.headerContent}>
          <h2 className={styles.headerTitle}>
            Ship web apps with the<br />
            {aiEnabled ? 'AI-enabled' : 'AI-ready'}{' '}
            <button
              className={styles.toggleBtn}
              aria-label="Toggle AI"
              onClick={() => setAiEnabled(!aiEnabled)}
            >
              <span className={`${styles.toggleTrack} ${!aiEnabled ? styles.toggleTrackOff : ''}`}>
                <span className={`${styles.toggleThumb} ${!aiEnabled ? styles.toggleThumbOff : ''}`} />
              </span>
            </button>
            {' '}framework
          </h2>
          {!aiEnabled && <p className={styles.headerSubtitle}>We're ready when you're ready</p>}
        </div>
        <div className={styles.headerGradient} />
        <div className={styles.headerLineTop} />
        <div className={styles.headerLine} />
        <div className={styles.headerLineLeft} />
        <div className={styles.headerLineRight} />
        <span className={styles.headerDotTL} />
        <span className={styles.headerDotTR} />
        <span className={styles.headerDotBL} />
        <span className={styles.headerDotBR} />
      </section>

      {/* Detail */}
      <section className={styles.detail}>
        <div className={styles.detailLineLeft} />
        <div className={styles.detailLineRight} />
        <div className={styles.detailLineBottom} />
        <span className={styles.detailDotBL} />
        <span className={styles.detailDotBR} />
        <div className={styles.container}>
          <div className={styles.splitLayout}>
            {/* Left: description */}
            <div className={styles.left}>
              <h3 className={styles.detailTitle}>
                A framework for<br />developers and agents
              </h3>
              <p className={styles.detailDescription}>
                Laravel has opinions on everything: routing, queues,<br />
                authentication, and more. That's thousands of<br />
                decisions an agent doesn't have to make. The result?<br />
                Clean code that anyone can understand.
              </p>
              <ul className={styles.featureList}>
                {features.map((f, i) => (
                  <li key={i}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M13.5 4.5L6.5 11.5L2.5 7.5" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
              <Link className={styles.ctaLink} to="/docs/12.x">
                Explore the framework
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M4 12L12 4M12 4H5M12 4v7" stroke="#f53003" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </Link>
            </div>

            {/* Right: code panel */}
            <div className={styles.right}>
              {/* Category tabs */}
              <div className={styles.categoryTabs}>
                {categories.map((cat, i) => (
                  <button
                    key={cat.name}
                    className={`${styles.categoryTab} ${i === activeCategory ? styles.categoryTabActive : ''}`}
                    onClick={() => { setActiveCategory(i); setActiveFile(0); }}
                  >
                    {cat.name}
                  </button>
                ))}
              </div>

              {/* Code editor */}
              <div className={styles.codeEditor}>
                <div className={styles.codeEditorInner}>
                  <div className={styles.fileTabs}>
                    {category.files.map((f, i) => (
                      <button
                        key={f.name}
                        className={`${styles.fileTab} ${i === activeFile ? styles.fileTabActive : ''}`}
                        onClick={() => setActiveFile(i)}
                      >
                        <svg className={`${styles.fileTabIcon} laravel-icon`} viewBox="0 0 50 50" fill="none">
                          <path fill="#f53003" fillRule="nonzero" d="M49.626 11.564a.809.809 0 0 1 .028.209v10.972a.8.8 0 0 1-.402.694l-9.209 5.302V39.25c0 .286-.152.55-.4.694L20.42 51.01c-.044.025-.092.041-.14.058-.018.006-.035.017-.054.022a.805.805 0 0 1-.41 0c-.022-.006-.042-.018-.063-.026-.044-.016-.09-.03-.132-.054L.402 39.944A.801.801 0 0 1 0 39.25V6.334c0-.072.01-.142.028-.21.006-.023.02-.044.028-.067.015-.042.029-.085.051-.124.015-.026.037-.047.055-.071.023-.032.044-.065.071-.093.023-.023.053-.04.079-.06.029-.024.055-.05.088-.069h.001l9.61-5.533a.802.802 0 0 1 .8 0l9.61 5.533h.002c.032.02.059.045.088.068.026.02.055.038.078.06.028.029.048.062.072.094.017.024.04.045.054.071.023.04.036.082.052.124.008.023.022.044.028.068a.809.809 0 0 1 .028.209v20.559l8.008-4.611v-10.51c0-.07.01-.141.028-.208.007-.024.02-.045.028-.068.016-.042.03-.085.052-.124.015-.026.037-.047.054-.071.024-.032.044-.065.072-.093.023-.023.052-.04.078-.06.03-.024.056-.05.088-.069h.001l9.611-5.533a.801.801 0 0 1 .8 0l9.61 5.533c.034.02.06.045.09.068.025.02.054.038.077.06.028.029.048.062.072.094.018.024.04.045.054.071.023.039.036.082.052.124.009.023.022.044.028.068zm-1.574 10.718v-9.124l-3.363 1.936-4.646 2.675v9.124l8.01-4.611zm-9.61 16.505v-9.13l-4.57 2.61-13.05 7.448v9.216l17.62-10.144zM1.602 7.719v31.068L19.22 48.93v-9.214l-9.204-5.209-.003-.002-.004-.002c-.031-.018-.057-.044-.086-.066-.025-.02-.054-.036-.076-.058l-.002-.003c-.026-.025-.044-.056-.066-.084-.02-.027-.044-.05-.06-.078l-.001-.003c-.018-.03-.029-.066-.042-.1-.013-.03-.03-.058-.038-.09v-.001c-.01-.038-.012-.078-.016-.117-.004-.03-.012-.06-.012-.09v-.002-21.481L4.965 9.654 1.602 7.72zm8.81-5.994L2.405 6.334l8.005 4.609 8.006-4.61-8.006-4.608zm4.164 28.764l4.645-2.674V7.719l-3.363 1.936-4.646 2.675v20.096l3.364-1.937zM39.243 7.164l-8.006 4.609 8.006 4.609 8.005-4.61-8.005-4.608zm-.801 10.605l-4.646-2.675-3.363-1.936v9.124l4.645 2.674 3.364 1.937v-9.124zM20.02 38.33l11.743-6.704 5.87-3.35-8-4.606-9.211 5.303-8.395 4.833 7.993 4.524z"/>
                        </svg>
                        {f.name}
                      </button>
                    ))}
                  </div>
                  <div className={styles.codeBody}>
                    {file.code}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
