import React, {useState, useCallback, type ReactNode} from 'react';
import './homepage.css';

function CheckIcon(): ReactNode {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18" className="check-icon" aria-hidden="true">
      <path fill="currentColor" fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
    </svg>
  );
}

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

/** Simple PHP syntax highlighter */
function highlightPhp(code: string): ReactNode[] {
  const lines = code.split('\n');
  let inBlockComment = false;
  return lines.map((line, lineIdx) => {
    const tokens: ReactNode[] = [];
    let remaining = line;
    let keyIdx = 0;

    if (inBlockComment) {
      const endIdx = remaining.indexOf('*/');
      if (endIdx !== -1) {
        tokens.push(<span key={keyIdx++} className="syn-comment">{remaining.slice(0, endIdx + 2)}</span>);
        remaining = remaining.slice(endIdx + 2);
        inBlockComment = false;
      } else {
        tokens.push(<span key={keyIdx++} className="syn-comment">{remaining}</span>);
        return <React.Fragment key={lineIdx}>{lineIdx > 0 && '\n'}{tokens}</React.Fragment>;
      }
    }

    while (remaining.length > 0) {
      // Block comment start
      const blockCommentMatch = remaining.match(/^(\/\*\*?)/);
      if (blockCommentMatch) {
        const endIdx = remaining.indexOf('*/', blockCommentMatch[1].length);
        if (endIdx !== -1) {
          tokens.push(<span key={keyIdx++} className="syn-comment">{remaining.slice(0, endIdx + 2)}</span>);
          remaining = remaining.slice(endIdx + 2);
        } else {
          tokens.push(<span key={keyIdx++} className="syn-comment">{remaining}</span>);
          inBlockComment = true;
          remaining = '';
        }
        continue;
      }

      // Single-line comment
      const commentMatch = remaining.match(/^(\/\/.*)/);
      if (commentMatch) {
        tokens.push(<span key={keyIdx++} className="syn-comment">{commentMatch[1]}</span>);
        remaining = remaining.slice(commentMatch[1].length);
        continue;
      }

      // HTML tags
      const htmlTagMatch = remaining.match(/^(<\/?)([\w-]+)/);
      if (htmlTagMatch) {
        tokens.push(<span key={keyIdx++} className="syn-html-tag">{htmlTagMatch[1]}</span>);
        tokens.push(<span key={keyIdx++} className="syn-html-tag">{htmlTagMatch[2]}</span>);
        remaining = remaining.slice(htmlTagMatch[0].length);
        continue;
      }

      const htmlCloseMatch = remaining.match(/^(\/?>)/);
      if (htmlCloseMatch) {
        tokens.push(<span key={keyIdx++} className="syn-html-tag">{htmlCloseMatch[1]}</span>);
        remaining = remaining.slice(htmlCloseMatch[1].length);
        continue;
      }

      // HTML attribute names
      const htmlAttrMatch = remaining.match(/^([a-zA-Z-]+)(?==)/);
      if (htmlAttrMatch && line.includes('<')) {
        tokens.push(<span key={keyIdx++} className="syn-html-attr">{htmlAttrMatch[1]}</span>);
        remaining = remaining.slice(htmlAttrMatch[1].length);
        continue;
      }

      // Blade echo braces {{ }}
      const bladeEchoMatch = remaining.match(/^(\{\{|\}\})/);
      if (bladeEchoMatch) {
        tokens.push(<span key={keyIdx++} className="syn-function">{bladeEchoMatch[1]}</span>);
        remaining = remaining.slice(bladeEchoMatch[1].length);
        continue;
      }

      // Blade directives
      const bladeMatch = remaining.match(/^(@(?:if|else|elseif|endif|foreach|endforeach|for|endfor|while|endwhile|unless|endunless|isset|endisset|empty|endempty|auth|endauth|guest|endguest|section|endsection|yield|extends|include|push|endpush|php|endphp|forelse|endforelse))\b/);
      if (bladeMatch) {
        tokens.push(<span key={keyIdx++} className="syn-type">{bladeMatch[1]}</span>);
        remaining = remaining.slice(bladeMatch[1].length);
        continue;
      }

      // HTML attribute strings (after =)
      const htmlAttrStr = tokens.length > 0 && remaining.match(/^("(?:[^"\\]|\\.)*")/);
      if (htmlAttrStr && line.includes('<')) {
        tokens.push(<span key={keyIdx++} className="syn-type">{htmlAttrStr[1]}</span>);
        remaining = remaining.slice(htmlAttrStr[1].length);
        continue;
      }

      // Strings (single or double quoted)
      const strMatch = remaining.match(/^('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")/);
      if (strMatch) {
        tokens.push(<span key={keyIdx++} className="syn-string">{strMatch[1]}</span>);
        remaining = remaining.slice(strMatch[1].length);
        continue;
      }

      // Numbers
      const numMatch = remaining.match(/^(\d+(?:\.\d+)?)\b/);
      if (numMatch) {
        tokens.push(<span key={keyIdx++} className="syn-number">{numMatch[1]}</span>);
        remaining = remaining.slice(numMatch[1].length);
        continue;
      }

      // Control flow keywords
      const ctrlMatch = remaining.match(/^(return|if|else|foreach|for|while|throw|catch|try|switch|case|break|continue)\b/);
      if (ctrlMatch) {
        tokens.push(<span key={keyIdx++} className="syn-control">{ctrlMatch[1]}</span>);
        remaining = remaining.slice(ctrlMatch[1].length);
        continue;
      }

      // PHP type keywords
      const typeMatch = remaining.match(/^(string|int|float|bool|array|void|null|mixed|never|true|false|self)\b/);
      if (typeMatch) {
        tokens.push(<span key={keyIdx++} className="syn-type">{typeMatch[1]}</span>);
        remaining = remaining.slice(typeMatch[1].length);
        continue;
      }

      // PHP keywords
      const kwMatch = remaining.match(/^(use|namespace|class|function|public|private|protected|new|extends|implements|static|readonly)\b/);
      if (kwMatch) {
        tokens.push(<span key={keyIdx++} className="syn-keyword">{kwMatch[1]}</span>);
        remaining = remaining.slice(kwMatch[1].length);
        // After use/namespace, treat the namespace path (excluding last segment) as plain text
        if (kwMatch[1] === 'use' || kwMatch[1] === 'namespace') {
          const nsMatch = remaining.match(/^( )((?:[A-Za-z_][A-Za-z0-9_]*\\)+)/);
          if (nsMatch) {
            tokens.push(nsMatch[1]);
            tokens.push(<span key={keyIdx++} className={kwMatch[1] === 'namespace' ? 'syn-class' : undefined}>{nsMatch[2]}</span>);
            remaining = remaining.slice(nsMatch[0].length);
          }
        }
        continue;
      }

      // $this keyword
      const thisMatch = remaining.match(/^(\$this)\b/);
      if (thisMatch) {
        tokens.push(<span key={keyIdx++} className="syn-type">{thisMatch[1]}</span>);
        remaining = remaining.slice(thisMatch[1].length);
        continue;
      }

      // PHP variables
      const varMatch = remaining.match(/^(\$[a-zA-Z_][a-zA-Z0-9_]*)/);
      if (varMatch) {
        tokens.push(<span key={keyIdx++} className="syn-variable">{varMatch[1]}</span>);
        remaining = remaining.slice(varMatch[1].length);
        continue;
      }

      // PHP attributes #[Name(...)]
      const attrMatch = remaining.match(/^(#\[)([A-Z][a-zA-Z0-9_]*)/);
      if (attrMatch) {
        tokens.push(<span key={keyIdx++}>{attrMatch[1]}</span>);
        tokens.push(<span key={keyIdx++}>{attrMatch[2]}</span>);
        remaining = remaining.slice(attrMatch[0].length);
        continue;
      }

      // Class/type references (PascalCase words)
      const classMatch = remaining.match(/^([A-Z][a-zA-Z0-9_]*)/);
      if (classMatch) {
        tokens.push(<span key={keyIdx++} className="syn-class">{classMatch[1]}</span>);
        remaining = remaining.slice(classMatch[1].length);
        continue;
      }

      // Fat arrow =>
      const fatArrowMatch = remaining.match(/^(=>)/);
      if (fatArrowMatch) {
        tokens.push(<span key={keyIdx++}>{fatArrowMatch[1]}</span>);
        remaining = remaining.slice(2);
        continue;
      }

      // Property/method access after ->
      const memberMatch = remaining.match(/^(->)([a-zA-Z_][a-zA-Z0-9_]*)/);
      if (memberMatch) {
        const isMethod = remaining[memberMatch[0].length] === '(';
        tokens.push(<span key={keyIdx++} className="syn-operator">{memberMatch[1]}</span>);
        tokens.push(<span key={keyIdx++} className={isMethod ? 'syn-method' : 'syn-variable'}>{memberMatch[2]}</span>);
        remaining = remaining.slice(memberMatch[0].length);
        continue;
      }

      // Static calls ::
      const staticMatch = remaining.match(/^(::)([a-zA-Z_][a-zA-Z0-9_]*)/);
      if (staticMatch) {
        tokens.push(<span key={keyIdx++} className="syn-operator">{staticMatch[1]}</span>);
        tokens.push(<span key={keyIdx++} className="syn-method">{staticMatch[2]}</span>);
        remaining = remaining.slice(staticMatch[0].length);
        continue;
      }

      // PHP tag
      const phpTag = remaining.match(/^(<\?php)/);
      if (phpTag) {
        tokens.push(<span key={keyIdx++} className="syn-keyword">{phpTag[1]}</span>);
        remaining = remaining.slice(phpTag[1].length);
        continue;
      }

      // PHP language constructs that look like functions
      const constructMatch = remaining.match(/^(echo|print|isset|unset|empty|die|exit|list)\b/);
      if (constructMatch) {
        tokens.push(<span key={keyIdx++} className="syn-function">{constructMatch[1]}</span>);
        remaining = remaining.slice(constructMatch[1].length);
        continue;
      }

      // Named arguments: word followed by :
      const namedArgMatch = remaining.match(/^([a-z_][a-zA-Z0-9_]*)(?=:)/);
      if (namedArgMatch) {
        tokens.push(<span key={keyIdx++} className="syn-named-arg">{namedArgMatch[1]}</span>);
        remaining = remaining.slice(namedArgMatch[1].length);
        continue;
      }

      // Function calls: word followed by (
      const funcMatch = remaining.match(/^([a-z_][a-zA-Z0-9_]*)\s*(?=\()/);
      if (funcMatch) {
        tokens.push(<span key={keyIdx++} className="syn-function">{funcMatch[0]}</span>);
        remaining = remaining.slice(funcMatch[0].length);
        continue;
      }

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
