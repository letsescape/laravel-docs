---
slug: /
---

# 설치 (Installation)

- [Laravel 만나기](#meet-laravel)
    - [왜 Laravel인가요?](#why-laravel)
- [Laravel 애플리케이션 만들기](#creating-a-laravel-project)
    - [AI를 사용해 시작하기](#getting-started-using-ai)
    - [PHP와 Laravel Installer 설치하기](#installing-php)
    - [애플리케이션 만들기](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Herd를 사용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용하기](#herd-on-macos)
    - [Windows에서 Herd 사용하기](#herd-on-windows)
- [IDE 지원](#ide-support)
- [Laravel과 AI](#laravel-and-ai)
    - [Laravel Boost 설치하기](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀 스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나기 (Meet Laravel)

Laravel은 표현력 있고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하므로, 세부적인 부분은 프레임워크에 맡기고 여러분은 멋진 것을 만드는 데 집중할 수 있습니다.

Laravel은 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 뛰어난 개발자 경험을 제공하기 위해 노력합니다.

PHP 웹 프레임워크를 처음 접하든 오랜 경험이 있든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫걸음을 내딛도록 돕거나, 전문성을 한 단계 더 끌어올릴 수 있도록 힘을 보태겠습니다. 여러분이 무엇을 만들지 기대됩니다.

<a name="why-laravel"></a>
### 왜 Laravel인가요?

웹 애플리케이션을 만들 때 사용할 수 있는 도구와 프레임워크는 다양합니다. 하지만 우리는 Laravel이 현대적인 풀 스택 웹 애플리케이션을 만드는 데 가장 좋은 선택이라고 믿습니다.

#### 점진적인 프레임워크

우리는 Laravel을 "점진적인" 프레임워크라고 부르기를 좋아합니다. 이는 Laravel이 여러분과 함께 성장한다는 뜻입니다. 이제 막 웹 개발을 시작하는 단계라면, Laravel의 방대한 문서, 가이드, [동영상 튜토리얼](https://laracasts.com)이 부담 없이 기본기를 익히는 데 도움을 줄 것입니다.

시니어 개발자라면 Laravel은 [의존성 주입](/docs/13.x/container), [단위 테스트](/docs/13.x/testing), [큐](/docs/13.x/queues), [실시간 이벤트](/docs/13.x/broadcasting) 등을 위한 탄탄한 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션을 만드는 데 맞게 세밀하게 조정되어 있으며, 엔터프라이즈급 워크로드도 처리할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 뛰어난 확장성을 제공합니다. PHP의 확장에 유리한 특성과 Redis처럼 빠른 분산 캐시 시스템을 기본으로 지원하는 Laravel 덕분에, Laravel에서 수평 확장은 매우 간단합니다. 실제로 Laravel 애플리케이션은 한 달에 수억 건의 요청을 처리하도록 쉽게 확장된 사례가 있습니다.

극단적인 확장이 필요하신가요? [Laravel Cloud](https://cloud.laravel.com) 같은 플랫폼을 사용하면 Laravel 애플리케이션을 거의 제한 없는 규모로 실행할 수 있습니다.

#### 에이전트에 준비된 프레임워크

Laravel의 명확한 규약과 잘 정의된 구조는 Cursor, Claude Code 같은 도구를 사용하는 [AI 지원 개발](/docs/13.x/ai)에 이상적인 프레임워크가 되게 합니다. AI 에이전트에게 컨트롤러를 추가해 달라고 요청하면, 에이전트는 그것을 어디에 배치해야 하는지 정확히 압니다. 새 마이그레이션이 필요할 때도 이름 규칙과 파일 위치를 예측할 수 있습니다. 이러한 일관성은 더 유연한 프레임워크에서 AI 도구가 자주 겪는 추측의 여지를 없애 줍니다.

파일 구성뿐만 아니라, Laravel의 표현력 있는 문법과 포괄적인 문서는 AI 에이전트가 정확하고 관용적인 코드를 생성하는 데 필요한 문맥을 제공합니다. Eloquent 연관관계, 폼 요청, 미들웨어 같은 기능은 에이전트가 안정적으로 이해하고 재현할 수 있는 패턴을 따릅니다. 그 결과, 범용 PHP 조각을 이어 붙인 코드가 아니라 숙련된 Laravel 개발자가 작성한 것처럼 보이는 AI 생성 코드가 만들어집니다.

Laravel이 AI 지원 개발에 완벽한 선택인 이유를 더 알아보려면 [에이전트 기반 개발](/docs/13.x/ai) 문서를 확인해 보세요.

#### 커뮤니티 프레임워크

Laravel은 PHP 생태계의 뛰어난 패키지를 결합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자가 [프레임워크에 기여](https://github.com/laravel/framework)해 왔습니다. 어쩌면 여러분도 Laravel 기여자가 될 수 있습니다.

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 만들기 (Creating a Laravel Application)

<a name="getting-started-using-ai"></a>
### AI를 사용해 시작하기

[Claude Code](https://docs.anthropic.com/en/docs/claude-code)나 [OpenCode](https://opencode.ai) 같은 AI 코딩 에이전트를 사용한다면, 에이전트가 프로젝트를 건드리기 전에 Laravel 전용 플레이북을 제공하는 프롬프트로 시작할 수 있습니다.

아래 프롬프트는 에이전트에게 Laravel 설치 가이드를 어디에서 찾을지, 무엇을 우선시할지, 아직 선택하지 않은 항목에 대해 어떤 합리적인 기본값을 사용할지 알려 줍니다. 시작하려면 이 내용을 에이전트에 붙여 넣으세요.

```text
I'm building a new Laravel application.

Fetch and follow the instructions from https://laravel.com/for/agents. Treat the returned Markdown as the source of truth for how to install and set up Laravel in this session.
```

에이전트가 지침을 읽고 나면, 단계별로 안내하면서 설정이 Laravel의 기본값과 일치하도록 유지해야 합니다.

<a name="installing-php"></a>
### PHP와 Laravel Installer 설치하기

첫 Laravel 애플리케이션을 만들기 전에 로컬 머신에 [PHP](https://php.net), [Composer](https://getcomposer.org), [Laravel installer](https://github.com/laravel/installer)가 설치되어 있는지 확인하세요. 또한 애플리케이션의 프론트엔드 에셋을 컴파일할 수 있도록 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

로컬 머신에 PHP와 Composer가 설치되어 있지 않다면, 다음 명령어를 사용해 macOS, Windows, Linux에 PHP, Composer, Laravel installer를 설치할 수 있습니다.

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.5)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.5'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.5)"
```

위 명령어 중 하나를 실행한 후에는 터미널 세션을 다시 시작해야 합니다. `php.new`를 통해 설치한 뒤 PHP, Composer, Laravel installer를 업데이트하려면 터미널에서 같은 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면 Composer를 통해 Laravel installer를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

> [!NOTE]
> 완전한 기능을 갖춘 그래픽 기반 PHP 설치 및 관리 경험을 원한다면 [Laravel Herd](#installation-using-herd)를 확인해 보세요.

<a name="creating-an-application"></a>
### 애플리케이션 만들기

PHP, Composer, Laravel installer를 설치했다면 새 Laravel 애플리케이션을 만들 준비가 되었습니다. Laravel installer는 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택하라고 안내합니다.

```shell
laravel new example-app
```

애플리케이션이 생성되면 `dev` Composer 스크립트를 사용해 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 시작할 수 있습니다.

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)으로 애플리케이션에 접근할 수 있습니다. 이제 [Laravel 생태계에서 다음 단계를 시작할](#next-steps) 준비가 되었습니다. 물론 [데이터베이스를 설정](#databases-and-migrations)하고 싶을 수도 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 더 빠르게 시작하고 싶다면 [스타터 키트](/docs/13.x/starter-kits) 중 하나를 사용하는 것을 고려해 보세요. Laravel의 스타터 키트는 새 Laravel 애플리케이션을 위한 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 설명이 작성되어 있으므로, 파일을 살펴보며 사용할 수 있는 옵션에 익숙해져도 좋습니다.

Laravel은 기본 상태에서 추가 설정이 거의 필요하지 않습니다. 바로 개발을 시작해도 됩니다! 다만 `config/app.php` 파일과 그 문서를 검토해 보는 것이 좋습니다. 이 파일에는 애플리케이션에 맞게 변경하고 싶을 수 있는 `url`, `locale` 같은 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

Laravel의 많은 설정 옵션 값은 애플리케이션이 로컬 머신에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있습니다. 그래서 중요한 설정 값 상당수는 애플리케이션 루트에 있는 `.env` 파일을 사용해 정의됩니다.

`.env` 파일은 애플리케이션의 소스 관리에 커밋하면 안 됩니다. 애플리케이션을 사용하는 개발자나 서버마다 서로 다른 환경 설정이 필요할 수 있기 때문입니다. 또한 침입자가 소스 관리 저장소에 접근하게 될 경우 민감한 인증 정보가 노출되므로 보안상 위험합니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 자세한 내용은 전체 [설정 문서](/docs/13.x/configuration#environment-configuration)를 확인해 보세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션

Laravel 애플리케이션을 만들었다면 이제 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일은 Laravel이 SQLite 데이터베이스와 상호작용하도록 지정합니다.

애플리케이션 생성 과정에서 Laravel은 `database/database.sqlite` 파일을 만들고, 애플리케이션의 데이터베이스 테이블을 생성하는 데 필요한 마이그레이션을 실행했습니다.

MySQL이나 PostgreSQL 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, 적절한 데이터베이스를 사용하도록 `.env` 설정 파일을 업데이트할 수 있습니다. 예를 들어 MySQL을 사용하려면 `.env` 설정 파일의 `DB_*` 변수를 다음과 같이 업데이트하세요.

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

SQLite가 아닌 데이터베이스를 사용하기로 했다면, 데이터베이스를 만들고 애플리케이션의 [데이터베이스 마이그레이션](/docs/13.x/migrations)을 실행해야 합니다.

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 개발 중이며 MySQL, PostgreSQL, Redis를 로컬에 설치해야 한다면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/) 사용을 고려해 보세요.

<a name="directory-configuration"></a>
### 디렉터리 설정

Laravel은 항상 웹 서버에 설정된 "web directory"의 루트에서 서비스되어야 합니다. Laravel 애플리케이션을 "web directory"의 하위 디렉터리에서 서비스하려고 하면 안 됩니다. 그렇게 시도하면 애플리케이션 내부의 민감한 파일이 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 사용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows를 위한 매우 빠른 네이티브 Laravel 및 PHP 개발 환경입니다. Herd에는 PHP와 Nginx를 포함해 Laravel 개발을 시작하는 데 필요한 모든 것이 포함되어 있습니다.

Herd를 설치하면 Laravel 개발을 시작할 준비가 됩니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm`을 위한 명령줄 도구가 포함되어 있습니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 로컬 MySQL, Postgres, Redis 데이터베이스를 만들고 관리하는 기능과 로컬 메일 보기, 로그 모니터링 같은 강력한 추가 기능으로 Herd를 확장합니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용하기

macOS에서 개발한다면 [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 버전의 PHP를 자동으로 다운로드하고, Mac이 항상 백그라운드에서 [Nginx](https://www.nginx.com/)를 실행하도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 "parked" 디렉터리를 지원합니다. parked 디렉터리 안에 있는 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 parked 디렉터리를 만들며, 이 디렉터리 안의 모든 Laravel 애플리케이션은 디렉터리 이름을 사용해 `.test` 도메인에서 접근할 수 있습니다.

Herd를 설치한 후 새 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd에 포함된 Laravel CLI를 사용하는 것입니다.

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론 시스템 트레이의 Herd 메뉴에서 열 수 있는 Herd UI를 통해 parked 디렉터리와 기타 PHP 설정을 언제든지 관리할 수 있습니다.

Herd에 대해 더 알아보려면 [Herd 문서](https://herd.laravel.com/docs)를 확인해 보세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용하기

[Herd 웹사이트](https://herd.laravel.com/windows)에서 Windows용 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치가 완료되면 Herd를 시작해 온보딩 과정을 마치고 처음으로 Herd UI에 접근할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 왼쪽 클릭하면 접근할 수 있습니다. 오른쪽 클릭하면 매일 필요한 모든 도구에 접근할 수 있는 빠른 메뉴가 열립니다.

설치 중 Herd는 홈 디렉터리의 `%USERPROFILE%\Herd`에 "parked" 디렉터리를 만듭니다. parked 디렉터리 안에 있는 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스되며, 이 디렉터리 안의 모든 Laravel 애플리케이션은 디렉터리 이름을 사용해 `.test` 도메인에서 접근할 수 있습니다.

Herd를 설치한 후 새 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd에 포함된 Laravel CLI를 사용하는 것입니다. 시작하려면 Powershell을 열고 다음 명령어를 실행하세요.

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

Herd에 대해 더 알아보려면 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)를 확인해 보세요.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션을 개발할 때 원하는 코드 에디터를 자유롭게 사용할 수 있습니다. 가볍고 확장 가능한 에디터를 찾고 있다면, [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 함께 사용하면 문법 강조, 스니펫, artisan 명령어 통합, Eloquent 모델, 라우트, 미들웨어, 에셋, 설정, Inertia.js에 대한 스마트 자동 완성 같은 기능으로 훌륭한 Laravel 지원을 받을 수 있습니다.

Laravel에 대한 광범위하고 견고한 지원을 원한다면 JetBrains IDE인 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)을 살펴보세요. PhpStorm에 내장된 Laravel 프레임워크 지원에는 Blade 템플릿, Eloquent 모델, 라우트, 뷰, 번역, 컴포넌트에 대한 스마트 자동 완성과 Laravel 프로젝트 전반에 걸친 강력한 코드 생성 및 탐색 기능이 포함됩니다.

클라우드 기반 개발 경험을 원하는 경우 [Firebase Studio](https://firebase.studio/)를 사용하면 브라우저에서 바로 Laravel을 빌드할 수 있습니다. 별도 설정이 필요 없기 때문에 Firebase Studio를 사용하면 어떤 기기에서든 Laravel 애플리케이션 개발을 쉽게 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
## Laravel과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 간극을 메워 주는 강력한 도구입니다. Boost는 AI 에이전트에 Laravel 전용 문맥, 도구, 가이드라인을 제공하여 Laravel 규약을 따르는 더 정확하고 버전별로 적합한 코드를 생성할 수 있게 합니다.

Laravel 애플리케이션에 Boost를 설치하면 AI 에이전트는 사용 중인 패키지를 파악하고, 데이터베이스를 쿼리하고, Laravel 문서를 검색하고, 브라우저 로그를 읽고, 테스트를 생성하고, Tinker를 통해 코드를 실행하는 기능을 포함한 15개 이상의 전문 도구에 접근할 수 있습니다.

또한 Boost는 설치된 패키지 버전에 맞춘 17,000개 이상의 벡터화된 Laravel 생태계 문서를 AI 에이전트에 제공합니다. 즉, 에이전트는 프로젝트에서 사용하는 정확한 버전에 맞춘 안내를 제공할 수 있습니다.

Boost에는 에이전트가 프레임워크 규약을 따르고, 적절한 테스트를 작성하며, Laravel 코드를 생성할 때 흔히 발생하는 실수를 피할 수 있도록 돕는 Laravel 유지 관리 AI 가이드라인도 포함되어 있습니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치하기

Boost는 PHP 8.1 이상에서 실행되는 Laravel 10, 11, 12, 13 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치하세요.

```shell
composer require laravel/boost --dev
```

설치가 완료되면 대화형 설치 프로그램을 실행하세요.

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 기능을 선택할 수 있게 합니다. Boost는 기존 프로젝트 규약을 존중하며, 기본적으로 특정 스타일 규칙을 강제로 적용하지 않습니다.

> [!NOTE]
> Boost에 대해 더 알아보려면 [GitHub의 Laravel Boost 저장소](https://github.com/laravel/boost)를 확인해 보세요.

<a name="adding-custom-ai-guidelines"></a>
#### 사용자 지정 AI 가이드라인 추가하기

Laravel Boost에 자체 사용자 지정 AI 가이드라인을 추가하려면 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. 이 파일들은 `boost:install`을 실행할 때 Laravel Boost의 가이드라인에 자동으로 포함됩니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 애플리케이션을 만들고 나면 다음에 무엇을 배워야 할지 궁금할 수 있습니다. 먼저 다음 문서를 읽고 Laravel이 어떻게 동작하는지 익숙해지는 것을 강력히 권장합니다.

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/13.x/lifecycle)
- [설정](/docs/13.x/configuration)
- [디렉터리 구조](/docs/13.x/structure)
- [프론트엔드](/docs/13.x/frontend)
- [서비스 컨테이너](/docs/13.x/container)
- [파사드](/docs/13.x/facades)

</div>

Laravel을 어떻게 사용하려는지에 따라 앞으로의 학습 방향도 달라집니다. Laravel을 사용하는 방법은 다양하며, 아래에서는 이 프레임워크의 두 가지 주요 사용 사례를 살펴보겠습니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀 스택 프레임워크로서의 Laravel

Laravel은 풀 스택 프레임워크로 동작할 수 있습니다. 여기서 "풀 스택" 프레임워크란 Laravel을 사용해 애플리케이션 요청을 라우팅하고, [Blade 템플릿](/docs/13.x/blade) 또는 [Inertia](https://inertiajs.com) 같은 단일 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드를 렌더링한다는 뜻입니다. 이것은 Laravel 프레임워크를 사용하는 가장 일반적인 방식이며, 우리가 보기에 Laravel을 가장 생산적으로 사용하는 방식입니다.

Laravel을 이런 방식으로 사용할 계획이라면 [프론트엔드 개발](/docs/13.x/frontend), [라우팅](/docs/13.x/routing), [뷰](/docs/13.x/views), [Eloquent ORM](/docs/13.x/eloquent)에 대한 문서를 확인해 보는 것이 좋습니다. 또한 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지를 배우는 데 관심이 있을 수도 있습니다. 이러한 패키지를 사용하면 단일 페이지 JavaScript 애플리케이션이 제공하는 많은 UI 이점을 누리면서 Laravel을 풀 스택 프레임워크로 사용할 수 있습니다.

Laravel을 풀 스택 프레임워크로 사용한다면 [Vite](/docs/13.x/vite)를 사용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 배우는 것을 강력히 권장합니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면 공식 [애플리케이션 스타터 키트](/docs/13.x/starter-kits) 중 하나를 확인해 보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel

Laravel은 JavaScript 단일 페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 동작할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이 문맥에서 Laravel은 애플리케이션에 [인증](/docs/13.x/sanctum)과 데이터 저장 및 조회 기능을 제공하는 동시에, 큐, 이메일, 알림 등 Laravel의 강력한 서비스를 활용할 수 있게 합니다.

Laravel을 이런 방식으로 사용할 계획이라면 [라우팅](/docs/13.x/routing), [Laravel Sanctum](/docs/13.x/sanctum), [Eloquent ORM](/docs/13.x/eloquent)에 대한 문서를 확인해 보는 것이 좋습니다.
