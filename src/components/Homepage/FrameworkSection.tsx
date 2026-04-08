import React, {useState, useCallback, type ReactNode} from 'react';
import {CheckIcon} from './SharedIcons';
import './homepage.css';

function LaravelFileIcon(): ReactNode {
  return (
    <span className="file-icon-wrapper" aria-hidden="true">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className="file-icon-svg">
        <path d="M12.51 5.49V8.78M9.64 3.89L12.5 5.49L15.24 3.96M6.5 12V15.5M3.5 3.5L6.5 2" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M3.5 10.5L9.5 7M9.5 7V3.5L12.51 2L15.5 3.5V7L12.44 8.5L9.5 7Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M0.5 2L3.5 0.5L6.5 2V8.5" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M0.5 2V12.17L6.5 15.5L12.52 12.09V8.5L6.5 12.04L3.5 10.5V3.5L0.5 2Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </span>
  );
}

/** Token rule: regex pattern, className, and optional capture group index */
type TokenRule = [RegExp, string | undefined, number?];

const SIMPLE_RULES: TokenRule[] = [
  [/^(\/\/.*)/, 'syn-comment'],
  [/^(\/?>)/, 'syn-html-tag'],
  [/^(\{\{|\}\})/, 'syn-function'],
  [/^(@(?:if|else|elseif|endif|foreach|endforeach|for|endfor|while|endwhile|unless|endunless|isset|endisset|empty|endempty|auth|endauth|guest|endguest|section|endsection|yield|extends|include|push|endpush|php|endphp|forelse|endforelse))\b/, 'syn-type'],
  [/^('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")/, 'syn-string'],
  [/^(\d+(?:\.\d+)?)\b/, 'syn-number'],
  [/^(return|if|else|foreach|for|while|throw|catch|try|switch|case|break|continue)\b/, 'syn-control'],
  [/^(string|int|float|bool|array|void|null|mixed|never|true|false|self)\b/, 'syn-type'],
  [/^(\$this)\b/, 'syn-type'],
  [/^(\$[a-zA-Z_][a-zA-Z0-9_]*)/, 'syn-variable'],
  [/^([A-Z][a-zA-Z0-9_]*)/, 'syn-class'],
  [/^(=>)/, undefined],
  [/^(<\?php)/, 'syn-keyword'],
  [/^(echo|print|isset|unset|empty|die|exit|list)\b/, 'syn-function'],
  [/^([a-z_][a-zA-Z0-9_]*)(?=:)/, 'syn-named-arg'],
  [/^([a-z_][a-zA-Z0-9_]*)\s*(?=\()/, 'syn-function'],
];

/** Simple PHP syntax highlighter */
function highlightPhp(code: string): ReactNode[] {
  const lines = code.split('\n');
  let inBlockComment = false;
  return lines.map((line, lineIdx) => {
    const tokens: ReactNode[] = [];
    let remaining = line;
    let keyIdx = 0;

    const pushToken = (text: string, cls?: string) => {
      tokens.push(cls ? <span key={keyIdx++} className={cls}>{text}</span> : <span key={keyIdx++}>{text}</span>);
    };

    if (inBlockComment) {
      const endIdx = remaining.indexOf('*/');
      if (endIdx !== -1) {
        pushToken(remaining.slice(0, endIdx + 2), 'syn-comment');
        remaining = remaining.slice(endIdx + 2);
        inBlockComment = false;
      } else {
        pushToken(remaining, 'syn-comment');
        return <React.Fragment key={lineIdx}>{lineIdx > 0 && '\n'}{tokens}</React.Fragment>;
      }
    }

    while (remaining.length > 0) {
      // Block comment start
      const blockCommentMatch = remaining.match(/^(\/\*\*?)/);
      if (blockCommentMatch) {
        const endIdx = remaining.indexOf('*/', blockCommentMatch[1].length);
        if (endIdx !== -1) {
          pushToken(remaining.slice(0, endIdx + 2), 'syn-comment');
          remaining = remaining.slice(endIdx + 2);
        } else {
          pushToken(remaining, 'syn-comment');
          inBlockComment = true;
          remaining = '';
        }
        continue;
      }

      // HTML tags (multi-capture)
      const htmlTagMatch = remaining.match(/^(<\/?)([\w-]+)/);
      if (htmlTagMatch) {
        pushToken(htmlTagMatch[1], 'syn-html-tag');
        pushToken(htmlTagMatch[2], 'syn-html-tag');
        remaining = remaining.slice(htmlTagMatch[0].length);
        continue;
      }

      // HTML attribute names (context-dependent)
      const htmlAttrMatch = remaining.match(/^([a-zA-Z-]+)(?==)/);
      if (htmlAttrMatch && line.includes('<')) {
        pushToken(htmlAttrMatch[1], 'syn-html-attr');
        remaining = remaining.slice(htmlAttrMatch[1].length);
        continue;
      }

      // HTML attribute strings (context-dependent)
      const htmlAttrStr = tokens.length > 0 && remaining.match(/^("(?:[^"\\]|\\.)*")/);
      if (htmlAttrStr && line.includes('<')) {
        pushToken(htmlAttrStr[1], 'syn-type');
        remaining = remaining.slice(htmlAttrStr[1].length);
        continue;
      }

      // PHP keywords with namespace handling
      const kwMatch = remaining.match(/^(use|namespace|class|function|public|private|protected|new|extends|implements|static|readonly)\b/);
      if (kwMatch) {
        pushToken(kwMatch[1], 'syn-keyword');
        remaining = remaining.slice(kwMatch[1].length);
        if (kwMatch[1] === 'use' || kwMatch[1] === 'namespace') {
          const nsMatch = remaining.match(/^( )((?:[A-Za-z_][A-Za-z0-9_]*\\)+)/);
          if (nsMatch) {
            tokens.push(nsMatch[1]);
            pushToken(nsMatch[2], kwMatch[1] === 'namespace' ? 'syn-class' : undefined);
            remaining = remaining.slice(nsMatch[0].length);
          }
        }
        continue;
      }

      // PHP attributes #[Name(...)]
      const attrMatch = remaining.match(/^(#\[)([A-Z][a-zA-Z0-9_]*)/);
      if (attrMatch) {
        pushToken(attrMatch[1]);
        pushToken(attrMatch[2]);
        remaining = remaining.slice(attrMatch[0].length);
        continue;
      }

      // Property/method access after ->
      const memberMatch = remaining.match(/^(->)([a-zA-Z_][a-zA-Z0-9_]*)/);
      if (memberMatch) {
        const isMethod = remaining[memberMatch[0].length] === '(';
        pushToken(memberMatch[1], 'syn-operator');
        pushToken(memberMatch[2], isMethod ? 'syn-method' : 'syn-variable');
        remaining = remaining.slice(memberMatch[0].length);
        continue;
      }

      // Static calls ::
      const staticMatch = remaining.match(/^(::)([a-zA-Z_][a-zA-Z0-9_]*)/);
      if (staticMatch) {
        pushToken(staticMatch[1], 'syn-operator');
        pushToken(staticMatch[2], 'syn-method');
        remaining = remaining.slice(staticMatch[0].length);
        continue;
      }

      // Try simple rules (single-capture patterns)
      let matched = false;
      for (const [regex, cls] of SIMPLE_RULES) {
        const m = remaining.match(regex);
        if (m) {
          pushToken(m[0], cls);
          remaining = remaining.slice(m[0].length);
          matched = true;
          break;
        }
      }
      if (matched) continue;

      // Default: consume one character
      tokens.push(remaining[0]);
      remaining = remaining.slice(1);
    }

    return (
      <React.Fragment key={lineIdx}>
        {lineIdx > 0 && '\n'}
        {tokens}
      </React.Fragment>
    );
  });
}

interface CodeCategory {
  name: string;
  files: {name: string; code: string}[];
}

const categories: CodeCategory[] = [
  {
    name: 'Auth',
    files: [
      {
        name: 'web.php',
        code: `Route::get('/dashboard', function (Request $request) {
    $user = $request->user();

    return view('dashboard', ['user' => $user]);
})->middleware('auth');`,
      },
      {
        name: 'UserController.php',
        code: `class FlightController
{
    #[Middleware('auth')]
    #[Authorize('view', 'flight')]
    public function show(Flight $flight): View
    {
        return view('dashboard', ['user' => $user]);
    }
}`,
      },
    ],
  },
  {
    name: 'AI SDK',
    files: [
      {
        name: 'api.php',
        code: `use App\\Ai\\Agents\\SalesCoach;
use Illuminate\\Http\\Request;

Route::post('/coach', function (Request $request) {
    $response = (new SalesCoach)
        ->prompt('Analyze this sales transcript...', attachments: [
            $request->file('transcript'),
        ]);

    return [
        'analysis' => (string) $response,
    ];
});`,
      },
      {
        name: 'SalesCoach.php',
        code: `namespace AppAiAgents;

use Laravel\\Ai\\ContractsAgent;
use Laravel\\Ai\\Promptable;
use Stringable;

class SalesCoach implements Agent
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback.';
    }
}`,
      },
    ],
  },
  {
    name: 'ORM',
    files: [
      {
        name: 'Flight.php',
        code: `namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Flight extends Model
{
    // ...
}`,
      },
      {
        name: 'web.php',
        code: `use App\\Models\\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}

Flight::create([
    'name' => 'New flight',
]);`,
      },
    ],
  },
  {
    name: 'Migrations',
    files: [
      {
        name: 'create_posts_table.php',
        code: `class CreatePostsTable extends Migration
{
    public function up()
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->text('content');
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->timestamps();
        });
    }
}`,
      },
    ],
  },
  {
    name: 'Validation',
    files: [
      {
        name: 'PostController.php',
        code: `class PostController
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        // ...
    }
}`,
      },
      {
        name: 'post.blade.php',
        code: `@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif`,
      },
    ],
  },
  {
    name: 'Storage',
    files: [
      {
        name: 'PostController.php',
        code: `class PostController
{
    public function store(Request $request)
    {
        if ($request->hasFile('image')) {
            $path = $request->file('image')->store('images', 'public');
        }
    }
}`,
      },
    ],
  },
  {
    name: 'Queues',
    files: [
      {
        name: 'ProcessPost.php',
        code: `class ProcessPost implements ShouldQueue
{
    public function handle()
    {
        $this->post->update([
            'rendered_content' => Str::markdown($this->post->content)
        ]);
    }
}`,
      },
      {
        name: 'PostController.php',
        code: `class PostController
{
    public function store(Request $request)
    {
        $post = Post::create($request->all());

        ProcessPost::dispatch($post);
    }
}`,
      },
    ],
  },
  {
    name: 'Testing',
    files: [
      {
        name: 'BasicTest.php',
        code: `it('can create a post', function () {
    $response = $this->post('/posts', [
        'title' => 'Test Post',
        'content' => 'This is a test post content.',
    ]);

    $response->assertStatus(302);

    $this->assertDatabaseHas('posts', [
        'title' => 'Test Post',
    ]);
});`,
      },
    ],
  },
];

export function AIFrameworkSection(): ReactNode {
  const [aiEnabled, setAiEnabled] = useState(true);

  return (
    <section className="ai-framework-section hp-section hp-section-bordered">
      <div className="container">
        <h2 className="ai-heading">
          Ship web apps with the<br />
          <span className="ai-heading-line2">
            {aiEnabled ? 'AI‑enabled' : 'AI‑ready'}{' '}
            <button
              className={`ai-toggle-inline ${aiEnabled ? 'ai-toggle--on' : ''}`}
              onClick={() => setAiEnabled(prev => !prev)}
              aria-pressed={aiEnabled}
              aria-label="Toggle AI"
            >
              <span className="ai-toggle-track">
                <span className="ai-toggle-thumb" />
              </span>
            </button>
            <br className="mobile-br" />{' '}framework
          </span>
        </h2>
        <p className={`ai-subtext ${aiEnabled ? 'ai-subtext--hidden' : ''}`}>We're ready when you're ready</p>
      </div>
    </section>
  );
}

export default function FrameworkSection(): ReactNode {
  const [activeCategory, setActiveCategory] = useState(0);
  const [activeFile, setActiveFile] = useState(0);

  const category = categories[activeCategory];
  const file = category.files[activeFile];

  const handleCategoryChange = (idx: number) => {
    setActiveCategory(idx);
    setActiveFile(0);
  };

  const codePanelRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const el = codePanelRef.current;
    if (!el) return;

    const wheelHandler = (e: WheelEvent) => {
      const canScrollY = el.scrollHeight > el.clientHeight;
      const canScrollX = el.scrollWidth > el.clientWidth;
      if (!canScrollY && !canScrollX) return;

      // Shift+Wheel converts vertical to horizontal
      const dx = e.shiftKey && e.deltaX === 0 ? e.deltaY : e.deltaX;
      const dy = e.shiftKey && e.deltaX === 0 ? 0 : e.deltaY;

      let shouldPrevent = false;

      if (canScrollY && dy !== 0) {
        const atTop = el.scrollTop <= 0 && dy < 0;
        const atBottom = el.scrollTop + el.clientHeight >= el.scrollHeight && dy > 0;
        if (!atTop && !atBottom) shouldPrevent = true;
      }

      if (canScrollX && dx !== 0) {
        const atLeft = el.scrollLeft <= 0 && dx < 0;
        const atRight = el.scrollLeft + el.clientWidth >= el.scrollWidth && dx > 0;
        if (!atLeft && !atRight) shouldPrevent = true;
      }

      if (shouldPrevent) {
        e.preventDefault();
        e.stopPropagation();
        el.scrollTop += dy;
        el.scrollLeft += dx;
      }
    };

    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartScrollLeft = 0;
    let touchStartScrollTop = 0;

    const touchStartHandler = (e: TouchEvent) => {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      touchStartScrollLeft = el.scrollLeft;
      touchStartScrollTop = el.scrollTop;
    };

    const touchMoveHandler = (e: TouchEvent) => {
      const canScrollY = el.scrollHeight > el.clientHeight;
      const canScrollX = el.scrollWidth > el.clientWidth;
      if (!canScrollY && !canScrollX) return;

      const dx = touchStartX - e.touches[0].clientX;
      const dy = touchStartY - e.touches[0].clientY;

      if (Math.abs(dx) > Math.abs(dy) && canScrollX) {
        e.preventDefault();
        el.scrollLeft = touchStartScrollLeft + dx;
      } else if (canScrollY) {
        const newTop = touchStartScrollTop + dy;
        const atTop = newTop <= 0 && dy < 0;
        const atBottom = newTop + el.clientHeight >= el.scrollHeight && dy > 0;
        if (!atTop && !atBottom) {
          e.preventDefault();
          el.scrollTop = newTop;
        }
      }
    };

    el.addEventListener('wheel', wheelHandler, {passive: false});
    el.addEventListener('touchstart', touchStartHandler, {passive: true});
    el.addEventListener('touchmove', touchMoveHandler, {passive: false});
    return () => {
      el.removeEventListener('wheel', wheelHandler);
      el.removeEventListener('touchstart', touchStartHandler);
      el.removeEventListener('touchmove', touchMoveHandler);
    };
  }, [activeCategory, activeFile]);

  return (
    <section className="framework-section hp-section hp-section-bordered">
      <div className="framework-section-gradient" />
      <div className="container framework-container">
        <div className="framework-grid">
          <div className="framework-info">
            <h3>A framework for{' '}<br className="not-mobile-br" />developers{' '}<br className="mobile-br" />and agents</h3>
            <p>
              Laravel has opinions on everything: routing, queues,{' '}<br className="tablet-br" /><br className="mobile-br" />authentication, and more. That's thousands of{' '}<br className="tablet-br" />decisions{' '}<br className="mobile-br" />an agent doesn't have to make. The result? Clean code{' '}<br className="mobile-br" />that anyone can understand.
            </p>
            <ul className="feature-list">
              <li><CheckIcon /> Starter kits for React, Vue, and Svelte</li>
              <li><CheckIcon /> AI SDK and Boost AI assistant</li>
              <li><CheckIcon /> Database ORM, queues, routing, and more</li>
              <li><CheckIcon /> Open source ecosystem of over 30 packages</li>
            </ul>
            <a href="https://laravel.com/docs/" className="explore-btn">
              Explore the framework
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16" className="explore-btn-icon">
                <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 0 0 1.06 0l7.22-7.22v5.69a.75.75 0 0 0 1.5 0v-7.5a.75.75 0 0 0-.75-.75h-7.5a.75.75 0 0 0 0 1.5h5.69l-7.22 7.22a.75.75 0 0 0 0 1.06Z" clipRule="evenodd" />
              </svg>
            </a>
          </div>

          <div className="code-area">
            {/* Category tabs - pill style */}
            <div className="category-tabs-wrapper">
              <ul className="category-tabs" role="toolbar" aria-label="Code categories">
                {categories.map((cat, idx) => (
                  <li key={cat.name} className="category-tab-item">
                    {idx === activeCategory && (
                      <div className="category-tab-bg" />
                    )}
                    <button
                      className={`category-tab ${idx === activeCategory ? 'category-tab--active' : ''}`}
                      aria-pressed={idx === activeCategory}
                      onClick={() => handleCategoryChange(idx)}
                    >
                      {cat.name}
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            {/* Code panel card */}
            <div className="code-card-outer">
              <div className="code-card">
                {/* File tabs */}
                <div className="file-tabs-bar">
                  <div className="file-tabs" role="tablist">
                    {category.files.map((f, idx) => (
                      <div key={f.name} className={`file-tab-wrapper ${idx > 0 ? 'file-tab-wrapper--border' : ''} ${idx === category.files.length - 1 ? 'file-tab-wrapper--border-right' : ''}`}>
                        <button
                          role="tab"
                          className={`file-tab ${idx === activeFile ? 'file-tab--active' : ''}`}
                          aria-selected={idx === activeFile}
                          onClick={() => setActiveFile(idx)}
                        >
                          <LaravelFileIcon />
                          <span className="file-tab-name">{f.name}</span>
                        </button>
                      </div>
                    ))}
                    <div className="file-tabs-fill" aria-hidden="true" />
                  </div>
                </div>

                {/* Code panel */}
                <div
                  role="tabpanel"
                  aria-label={file.name}
                  className="code-panel"
                  ref={codePanelRef}
                >
                  <pre>
                    <code>{highlightPhp(file.code)}</code>
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
