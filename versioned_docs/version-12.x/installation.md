# 설치 (Installation)

- [라라벨 만나보기](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 라라벨 설치 도구 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 환경설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스 및 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서의 Herd](#herd-on-macos)
    - [Windows에서의 Herd](#herd-on-windows)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 만나보기 (Meet Laravel)

라라벨(Laravel)은 표현력이 뛰어나고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크란, 애플리케이션을 만들 때 구조와 출발점을 제공하여, 여러분이 세세한 부분까지 신경 쓰지 않고도 멋진 것을 만드는 데 집중할 수 있게 도와주는 도구입니다.

라라벨은 강력한 기능과 함께 뛰어난 개발자 경험을 제공하기 위해 노력합니다. 예를 들어 철저한 의존성 주입, 표현력 높은 데이터베이스 추상화 레이어, 큐와 예약 작업, 단위 및 통합 테스트 등 다양한 기능을 제공합니다.

PHP 웹 프레임워크가 처음인 분이든, 다년간의 경험을 가진 개발자이든, 라라벨은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫 걸음을 내딛도록 돕거나, 여러분의 역량을 한 단계 더 성장시킬 수 있도록 지원합니다. 여러분이 라라벨로 어떤 것을 만들어낼지 기대됩니다.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 선택할 수 있는 도구와 프레임워크는 다양합니다. 하지만 저희는 라라벨이 현대적이고, 풀스택 웹 애플리케이션을 구축하기에 가장 적합한 선택이라고 믿습니다.

#### 점진적 프레임워크

라라벨은 "점진적(progressive)" 프레임워크로 불리기도 합니다. 이는 라라벨이 여러분과 함께 성장할 수 있다는 뜻입니다. 웹 개발에 첫발을 들이는 단계라면, 라라벨의 방대한 공식 문서, 가이드, [동영상 튜토리얼](https://laracasts.com) 덕분에 부담 없이 기본기를 익힐 수 있습니다.

경험이 풍부한 시니어 개발자라면, 라라벨은 [의존성 주입](/docs/12.x/container), [단위 테스트](/docs/12.x/testing), [큐 작업](/docs/12.x/queues), [실시간 이벤트](/docs/12.x/broadcasting) 등 전문가용 도구를 제공합니다. 라라벨은 전문적인 웹 애플리케이션 구축에 최적화되어 있으며, 엔터프라이즈 규모의 트래픽도 거뜬히 처리할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

라라벨은 매우 뛰어난 확장성을 자랑합니다. PHP의 확장 친화적인 특성과, Redis와 같은 빠르고 분산된 캐시 시스템을 라라벨에서 기본적으로 지원하기 때문에, 라라벨로 수평 확장이 매우 쉽게 가능합니다. 실제로, 라라벨 애플리케이션은 월 수억 건의 요청을 처리하도록 쉽게 확장된 사례가 있습니다.

더 극단적인 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com) 같은 플랫폼을 이용해 거의 무제한에 가까운 규모로 라라벨 애플리케이션을 운영할 수 있습니다.

#### 에이전트 친화적 프레임워크

라라벨은 명확한 규칙과 잘 정의된 구조를 갖추고 있어, Cursor나 Claude Code와 같은 도구를 활용한 [AI 지원 개발](/docs/12.x/ai)에 최적화되어 있습니다. 예를 들어, AI 에이전트에게 컨트롤러를 추가하라고 명령하면, 어디에 추가해야 하는지 정확히 알 수 있습니다. 마이그레이션 파일 역시 이름 규칙과 디렉터리 구조가 예측 가능해 AI 도구가 실수 없이 작업을 수행할 수 있습니다.

파일 구조뿐만 아니라, 표현력 있는 문법과 포괄적인 문서 덕분에 AI 에이전트는 필요한 맥락 정보를 충분히 얻어 올바른 코드, 즉 라라벨 스타일의 코드를 만들어낼 수 있습니다. Eloquent 연관 관계, 폼 리퀘스트, 미들웨어와 같은 기능 역시 예측 가능한 패턴을 따르므로, AI가 쉽게 이해하고 활용할 수 있습니다. 그 결과, AI가 작성한 코드도 숙련된 라라벨 개발자가 작성한 것처럼 자연스럽게 만들어집니다.

AI 지원 개발에 이상적인 프레임워크로서의 라라벨에 대해 더 알고 싶다면 [에이전틱 개발(agentic development)](/docs/12.x/ai) 문서를 참고하세요.

#### 커뮤니티 프레임워크

라라벨은 PHP 생태계의 우수한 패키지들을 결합하여, 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 전 세계 수많은 뛰어난 개발자들이 라라벨에 [직접 기여](https://github.com/laravel/framework)하고 있습니다. 여러분도 언젠가 라라벨에 기여하게 될지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 라라벨 설치 도구 설치 (Installing PHP and the Laravel Installer)

처음 라라벨 애플리케이션을 만들기 전에, 로컬 머신에 [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [라라벨 설치 도구](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한, 애플리케이션의 프론트엔드 자산을 컴파일하기 위해 [Node 및 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

만약 로컬 머신에 PHP와 Composer가 설치되어 있지 않다면, 아래 명령어로 macOS, Windows, Linux에서 PHP, Composer, 라라벨 설치 도구를 한 번에 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

위 명령어 중 하나를 실행한 후에는 터미널 세션을 다시 시작하세요. 추후 PHP, Composer, 라라벨 설치 도구를 `php.new`로 설치한 이후에도, 위 명령어를 다시 실행하면 업데이트할 수 있습니다.

이미 PHP와 Composer가 설치되어 있다면 Composer로 라라벨 설치 도구만 따로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 보다 완벽한 기능과 그래픽 기반의 PHP 설치/관리를 원한다면 [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, 라라벨 설치 도구 설치가 끝났다면 이제 새로운 라라벨 애플리케이션을 바로 만들 수 있습니다. 라라벨 설치 도구는 원하는 테스트 프레임워크, 데이터베이스, 스타터 키트 등을 선택할 수 있도록 안내합니다:

```shell
laravel new example-app
```

애플리케이션이 만들어지면, `dev` Composer 스크립트로 라라벨의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 실행할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버가 실행되면, 애플리케이션은 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 접속 가능합니다. 이제 [라라벨 생태계의 다음 단계에 도전](#next-steps)할 준비가 되었습니다. 물론 [데이터베이스 설정](#databases-and-migrations)도 원하실 수 있습니다.

> [!NOTE]
> 라라벨 애플리케이션 개발을 빠르게 시작하고 싶다면 [스타터 키트](/docs/12.x/starter-kits)를 사용해 보세요. 라라벨의 스타터 키트는 인증 시스템(백엔드/프론트엔드 포함)을 빠르게 적용할 수 있습니다.

<a name="initial-configuration"></a>
## 초기 환경설정 (Initial Configuration)

라라벨 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 설명이 잘 달려 있으니 언제든 파일을 살펴보며 설정 가능한 옵션을 익혀보세요.

라라벨은 기본값 그대로도 대부분의 경우 별도의 추가 설정이 필요하지 않습니다. 바로 개발을 시작하실 수 있습니다! 하지만, `config/app.php` 파일과 그 문서도 한번 확인해 보시기 바랍니다. 예를 들어 `url`, `locale` 등 애플리케이션 특성에 따라 변경할 수 있는 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

라라벨의 설정 값은 로컬 머신에서 실행하는지, 운영 서버에서 실행하는지에 따라 값이 달라질 수 있습니다. 그래서 중요한 설정 값들은 애플리케이션 루트의 `.env` 파일을 통해 지정하는 것이 일반적입니다.

`.env` 파일은 개발자나 서버별 환경이 다를 수 있으므로 애플리케이션의 소스 관리 시스템(예: Git)에는 커밋하지 않는 것이 좋습니다. 만약 소스 저장소에 `.env` 파일이 노출되면, 중요한 인증 정보가 외부로 유출될 위험이 있기 때문입니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대해 더 자세히 알고 싶다면 [설정 문서](/docs/12.x/configuration#environment-configuration)를 참고하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스 및 마이그레이션 (Databases and Migrations)

라라벨 애플리케이션을 만들었다면 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 여러분의 `.env` 설정 파일에는 라라벨이 SQLite 데이터베이스를 사용하도록 지정되어 있습니다.

애플리케이션을 생성하는 과정에서 라라벨이 자동으로 `database/database.sqlite` 파일을 만들고, 마이그레이션을 실행해 필요한 데이터베이스 테이블도 초기화합니다.

MySQL이나 PostgreSQL 등 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 설정 파일에서 적절한 정보를 아래와 같이 수정하면 됩니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite 이외 데이터베이스를 사용한다면, 직접 데이터베이스를 생성하고 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS나 Windows에서 MySQL, PostgreSQL, Redis 등을 로컬에 설치하고 싶다면, [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 이용해 보세요.

<a name="directory-configuration"></a>
### 디렉터리 설정 (Directory Configuration)

라라벨은 반드시 웹 서버의 "웹 디렉터리" 루트에서 서비스되어야 합니다. 웹 디렉터리의 하위 디렉터리에서 라라벨 애플리케이션을 실행하려고 해서는 안 됩니다. 그렇게 할 경우 애플리케이션에 포함된 민감한 파일들이 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용할 수 있는 매우 빠르고, 네이티브한 라라벨·PHP 개발 환경입니다. Herd에는 라라벨 개발에 필요한 PHP, Nginx 등이 모두 포함되어 있습니다.

Herd를 설치하면 바로 라라벨 개발을 시작할 수 있습니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 개발에 필요한 명령줄 도구가 기본 제공됩니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 강력한 추가 기능을 제공합니다. 예를 들어, 로컬 MySQL, Postgres, Redis 데이터베이스 생성/관리, 메일 뷰잉, 로그 모니터링 기능 등이 포함되어 있습니다.

<a name="herd-on-macos"></a>
### macOS에서의 Herd (Herd on macOS)

macOS에서 개발한다면 [Herd 웹사이트](https://herd.laravel.com)에서 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 버전의 PHP를 자동으로 다운로드하고, Mac에서 [Nginx](https://www.nginx.com/)가 항상 백그라운드에서 실행되도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "파킹된" 디렉터리를 지원합니다. 파킹된 디렉터리 내의 라라벨 애플리케이션은 자동으로 Herd에서 서비스됩니다. 기본적으로 Herd는 `~/Herd` 경로에 파킹 디렉터리를 만드며, 이곳에 있는 라라벨 애플리케이션은 디렉터리 명을 그대로 사용해 `.test` 도메인에서 접근할 수 있습니다.

Herd를 설치한 뒤, 새로운 라라벨 애플리케이션을 만들 때는 Herd와 함께 제공되는 라라벨 CLI를 활용하는 것이 가장 빠릅니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론 시스템 트레이의 Herd 메뉴에서 Herd UI를 열어 파킹 디렉터리나 기타 PHP 설정을 직접 관리할 수도 있습니다.

Herd에 대해 더 알고 싶다면 [Herd 공식 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서의 Herd (Herd on Windows)

[Herd 웹사이트](https://herd.laravel.com/windows)에서 Windows용 설치 프로그램을 다운로드할 수 있습니다. 설치가 완료되면 Herd를 실행해 온보딩 절차를 마치고, Herd UI에 처음으로 접속할 수 있습니다.

Herd UI는 시스템 트레이에 있는 Herd 아이콘을 왼쪽 클릭해서 열 수 있으며, 오른쪽 클릭하면 필요한 여러 도구에 빠르게 접근할 수 있는 메뉴가 나타납니다.

설치 중 Herd는 홈 디렉터리의 `%USERPROFILE%\Herd`에 "파킹된" 디렉터리를 생성합니다. 이 디렉터리 안에 있는 모든 라라벨 애플리케이션은 Herd에 의해 자동으로 서비스되며, 디렉터리 이름을 사용해 `.test` 도메인으로 쉽게 접근할 수 있습니다.

설치 후에는 Herd에 포함된 라라벨 CLI로 새로운 라라벨 애플리케이션을 만들 수 있습니다. PowerShell을 열고 아래 명령어를 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Herd에 대한 더 자세한 내용은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 참고하세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

라라벨 애플리케이션 개발에는 원하는 어떤 코드 에디터도 자유롭게 사용할 수 있습니다. 가볍고 확장성 있는 에디터를 원한다면 [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [Laravel VS Code 확장](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 추가해서 사용해 보세요. 라라벨 전용 문법 하이라이팅, 코드 스니펫, 아티즌 명령어 통합, Eloquent 모델/라우트/미들웨어/에셋/설정/Inertia.js 자동완성 등 강력한 기능을 지원합니다.

좀 더 강력하고 깊이 있는 라라벨 지원을 원한다면 JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)을 추천합니다. Blade 템플릿, Eloquent 모델/라우트/뷰/다국어/컴포넌트 자동완성, 강력한 코드 생성 및 프로젝트 전체 네비게이션 등 라라벨을 위한 내장 기능을 제공합니다.

클라우드 기반 개발 경험이 필요하다면 [Firebase Studio](https://firebase.studio/)를 활용해 브라우저에서 바로 라라벨 개발을 할 수 있습니다. 별도 셋업 없이, 언제 어디서든 즉시 라라벨 프로젝트를 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 라라벨 애플리케이션 사이의 장벽을 허물어주는 강력한 도구입니다. Boost는 AI 에이전트에게 라라벨만의 맥락, 도구, 지침을 제공하여, 라라벨 규칙 및 버전에 맞는 더 정확한 코드를 만들어낼 수 있게 도와줍니다.

Boost를 애플리케이션에 설치하면, AI 에이전트가 사용할 수 있는 15개 이상의 전용 도구가 추가됩니다. 사용 중인 패키지 확인, 데이터베이스 쿼리, 라라벨 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등이 가능합니다.

또한 Boost는 프로젝트별로 설치된 패키지 버전에 맞는 1만 7천개 이상의 벡터화된 라라벨 생태계 문서 데이터를 AI 에이전트에 제공합니다. 덕분에 AI가 프로젝트에 딱 맞는 버전의 정보를 기반으로 더 정확한 도움을 줄 수 있습니다.

Boost에는 라라벨에서 직접 관리하는 AI 개발 지침이 함께 제공되어, 에이전트가 프레임워크 규칙을 잘 따르고, 적절한 테스트 코드를 작성하며, 코드 생성 시 흔히 저지르는 실수를 방지할 수 있습니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상을 사용하는 라라벨 10, 11, 12 버전에서 설치할 수 있습니다. 다음 명령어로 개발 의존성으로 Boost를 추가하세요:

```shell
composer require laravel/boost --dev
```

설치가 끝나면, 상호작용형 인스톨러를 실행합니다:

```shell
php artisan boost:install
```

인스톨러는 여러분의 IDE와 AI 에이전트를 자동 감지하며, 프로젝트에 적합한 기능들을 선택적으로 활성화할 수 있습니다. Boost는 기존 프로젝트 규칙을 존중하며, 기본적으로 스타일 규칙을 강제하지 않습니다.

> [!NOTE]
> Boost에 대해 더 알아보려면 [Laravel Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
#### 커스텀 AI 지침 추가하기

Laravel Boost에 직접 만든 AI 지침을 추가하고 싶다면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 넣으면 됩니다. 이 파일들은 `boost:install` 명령 실행 시 Boost의 기본 지침과 함께 자동으로 적용됩니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

이제 라라벨 애플리케이션을 만들었으니, 앞으로 무엇을 공부하고 개발할지 고민하실 수 있습니다. 먼저, 라라벨이 어떻게 동작하는지 익히기 위해 다음 문서를 꼭 읽어보시길 추천합니다:

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/12.x/lifecycle)
- [설정](/docs/12.x/configuration)
- [디렉터리 구조](/docs/12.x/structure)
- [프론트엔드](/docs/12.x/frontend)
- [서비스 컨테이너](/docs/12.x/container)
- [파사드](/docs/12.x/facades)

</div>

여러분이 라라벨을 어떻게 사용하고 싶은지에 따라서도 앞으로의 학습 방향이 달라집니다. 라라벨 프레임워크를 활용하는 대표적인 두 가지 방식을 아래에서 소개합니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

라라벨을 풀스택 프레임워크로 사용할 수 있습니다. 여기서 "풀스택"이라는 것은, 라라벨로 요청을 처리하고, [Blade 템플릿](/docs/12.x/blade)이나 [Inertia](https://inertiajs.com) 같은 SPA 하이브리드 기술로 프론트엔드까지 직접 렌더링하는 방식을 의미합니다. 가장 일반적이고, 저희가 생각하기에도 가장 생산적인 라라벨 사용 방식입니다.

이 방식으로 라라벨을 사용할 계획이라면 [프론트엔드 개발](/docs/12.x/frontend), [라우팅](/docs/12.x/routing), [뷰](/docs/12.x/views), [Eloquent ORM](/docs/12.x/eloquent) 문서를 확인해 보세요. 또한, 커뮤니티 패키지인 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)도 추천합니다. 이 패키지들은 라라벨 풀스택 프레임워크 환경에서, SPA가 주는 UI의 장점도 함께 누릴 수 있게 해 줍니다.

풀스택 프레임워크로 라라벨을 사용할 때는 [Vite](/docs/12.x/vite)로 CSS, 자바스크립트 자산을 빌드하는 방법도 꼭 익히시기 바랍니다.

> [!NOTE]
> 애플리케이션 개발을 더 빠르게 시작하고 싶다면 공식 [스타터 키트](/docs/12.x/starter-kits)를 확인해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

라라벨은 자바스크립트 싱글 페이지 애플리케이션(SPA)이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 라라벨을 사용할 수 있습니다. 이 경우, 라라벨은 [인증](/docs/12.x/sanctum)과 데이터 저장/조회 기능은 물론, 큐, 이메일, 알림 등 다양한 강력한 서비스를 제공합니다.

이와 같이 라라벨을 API 백엔드로 활용한다면, [라우팅](/docs/12.x/routing), [Laravel Sanctum](/docs/12.x/sanctum), [Eloquent ORM](/docs/12.x/eloquent)에 관한 문서를 참고해 보세요.