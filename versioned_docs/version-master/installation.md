# 설치 (Installation)

- [라라벨 알아보기](#meet-laravel)
    - [왜 라라벨인가?](#why-laravel)
- [라라벨 애플리케이션 생성](#creating-a-laravel-project)
    - [PHP 및 Laravel 설치기 설치](#installing-php)
    - [애플리케이션 생성](#creating-an-application)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 구성](#directory-configuration)
- [Herd를 이용한 설치](#installation-using-herd)
    - [macOS에서 Herd 사용](#herd-on-macos)
    - [Windows에서 Herd 사용](#herd-on-windows)
- [IDE 지원](#ide-support)
- [라라벨과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 라라벨](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 라라벨](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 알아보기 (Meet Laravel)

Laravel은 표현적이고 우아한 문법을 제공하는 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션 개발의 구조와 시작점을 제공하여, 여러분이 세세한 부분에 신경쓰지 않고도 멋진 것을 만드는 데 집중할 수 있도록 돕습니다.

Laravel은 탁월한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐 및 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 훌륭한 개발자 경험을 목표로 하고 있습니다.

PHP 웹 프레임워크가 처음이든, 오랜 경력을 가진 개발자이든 Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 저희는 여러분이 웹 개발자로서 첫 발을 내딛을 수 있도록 돕거나, 더 높은 전문성을 추구하는 데 도약할 수 있도록 지원합니다. 여러분이 무엇을 만들어내실지 기대됩니다.

<a name="why-laravel"></a>
### 왜 라라벨인가? (Why Laravel?)

웹 애플리케이션을 개발할 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 저희는 Laravel이 최신의 풀스택 웹 애플리케이션을 구축하는 데 가장 이상적인 선택이라고 믿습니다.

#### 점진적(Progressive) 프레임워크

저희는 Laravel을 “점진적” 프레임워크라고 부릅니다. 이는 Laravel이 여러분과 함께 성장한다는 의미입니다. 웹 개발을 처음 시작하는 분이라면, Laravel의 방대한 공식 문서, 가이드, 그리고 [영상 강좌](https://laracasts.com) 덕분에 압도되지 않고 기초를 배울 수 있습니다.

시니어 개발자에게 Laravel은 [의존성 주입](/docs/master/container), [단위 테스트](/docs/master/testing), [큐](/docs/master/queues), [실시간 이벤트](/docs/master/broadcasting) 등 robust(강력한) 도구들을 제공합니다. Laravel은 전문적인 웹 애플리케이션 개발에 최적화되어 있으며, 엔터프라이즈 수준의 워크로드까지도 무리 없이 소화할 수 있습니다.

#### 뛰어난 확장성(Scalable Framework)

Laravel은 확장성이 매우 뛰어납니다. PHP의 확장 친화적 특성과, Redis와 같은 빠른 분산 캐시 시스템에 대한 Laravel의 내장 지원 덕분에, Laravel로 수평 확장은 매우 간단합니다. 실제로, Laravel 애플리케이션은 한 달에 수억 건의 요청을 손쉽게 처리할 수 있을 정도로 규모를 확장할 수 있습니다.

극한의 확장이 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 플랫폼을 사용하여 거의 제한 없는 규모로 Laravel 애플리케이션을 운영할 수 있습니다.

#### AI 에이전트 친화적(Agent Ready Framework)

Laravel은 고유한 규칙과 명확하게 정의된 구조를 지니고 있어, Cursor, Claude Code와 같은 도구를 사용한 [AI 지원 개발](/docs/master/ai)에 이상적입니다. 예를 들어, 컨트롤러를 추가하도록 AI 에이전트에게 요청하면, 어디에 배치해야 할지 명확하게 파악할 수 있습니다. 네임 규칙과 파일 위치가 예측 가능하므로, 마이그레이션을 추가할 때도 정확하게 처리할 수 있습니다. 이러한 일관성은 좀 더 유연한 프레임워크에서 흔히 AI 툴이 혼란스러워하는 부분을 해소해 줍니다.

파일 구조 뿐만 아니라, Laravel의 표현력 있는 문법과 방대한 문서 덕분에, AI 에이전트는 올바르고 표준적인 코드를 생성할 수 있는 충분한 맥락을 가집니다. Eloquent 연관관계, 폼 요청, 미들웨어 등의 기능은 일관된 패턴에 따라 작성되므로, 에이전트가 신뢰성 높게 이해하고 재현할 수 있습니다. 그 결과, AI가 생성한 코드는 경험 많은 Laravel 개발자가 작성한 코드를 방불케 합니다.

AI 지원 개발에 Laravel이 왜 완벽한 선택이 될 수 있는지 자세한 내용은 [AI 에이전트 기반 개발](/docs/master/ai) 문서를 참고하세요.

#### 개발자 커뮤니티(Community Framework)

Laravel은 PHP 생태계에서 최고의 패키지들을 결합하여, 가장 안정적이고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)했습니다. 어쩌면 여러분도 Laravel 기여자가 될 수 있을지도 모릅니다.

<a name="creating-a-laravel-project"></a>
## 라라벨 애플리케이션 생성 (Creating a Laravel Application)

<a name="installing-php"></a>
### PHP 및 Laravel 설치기 설치 (Installing PHP and the Laravel Installer)

처음 Laravel 애플리케이션을 만들기 전에, [PHP](https://php.net), [Composer](https://getcomposer.org), 그리고 [Laravel 설치기](https://github.com/laravel/installer)가 로컬에 설치되어 있는지 확인해야 합니다. 또한, 애플리케이션의 프런트엔드 에셋을 빌드하기 위해 [Node와 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/)도 설치해야 합니다.

만약 PHP와 Composer가 아직 설치되어 있지 않다면, macOS, Windows, Linux에서 아래 명령어를 통해 PHP, Composer, Laravel 설치기를 설치할 수 있습니다:

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

위 명령어를 실행한 후에는 터미널 세션을 재시작해야 합니다. 설치 후, `php.new`를 통해 PHP, Composer, Laravel 설치기를 업데이트하려면, 터미널에서 위와 동일한 명령어를 다시 실행하면 됩니다.

이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치기를 아래와 같이 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

> [!NOTE]
> 완전한 그래픽 기반의 PHP 설치 및 관리 환경이 필요하다면, [Laravel Herd](#installation-using-herd)를 참고하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성 (Creating an Application)

PHP, Composer, Laravel 설치기를 모두 설치했다면 이제 새로운 Laravel 애플리케이션을 만들 준비가 완료되었습니다. Laravel 설치기를 통해 선호하는 테스트 프레임워크, 데이터베이스, 스타터 키트를 선택할 수 있습니다:

```shell
laravel new example-app
```

애플리케이션이 생성된 후에는, `dev` Composer 스크립트를 사용하여 Laravel의 로컬 개발 서버, 큐 워커, Vite 개발 서버를 시작할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)에서 애플리케이션에 접속할 수 있습니다. 이제 [다음 단계로 Laravel 생태계에 진입](#next-steps)할 준비가 되었습니다. 물론, 추가로 [데이터베이스 설정](#databases-and-migrations)을 진행할 수도 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 좀 더 빠르게 시작하고 싶다면, [스타터 키트](/docs/master/starter-kits)를 이용하는 것도 좋은 선택입니다. Laravel의 스타터 키트는 백엔드 및 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 설정 옵션에는 설명이 달려 있으므로, 파일을 살펴보며 어떤 옵션이 있는지 익혀두는 것이 좋습니다.

Laravel은 처음부터 거의 추가적인 설정 없이 바로 사용이 가능합니다. 바로 개발을 시작할 수 있습니다! 하지만, 필요에 따라 `config/app.php` 파일과 관련 설명서를 검토해 볼 수도 있습니다. 이 파일에는 `url`, `locale` 등 애플리케이션에 맞게 조정할 수 있는 다양한 옵션이 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정 (Environment Based Configuration)

Laravel의 많은 설정 값은 애플리케이션이 로컬 머신에서 실행되고 있는지, 또는 운영 서버에서 실행 중인지에 따라 달라질 수 있습니다. 이런 이유로, 주요 설정 값들은 애플리케이션 루트에 위치한 `.env` 파일을 통해 정의됩니다.

`.env` 파일은 애플리케이션의 소스 컨트롤에 포함시키지 않는 것이 좋습니다. 애플리케이션을 사용하는 각 개발자/서버마다 서로 다른 환경 설정이 필요할 수 있기 때문입니다. 또한, 소스 컨트롤 저장소에 침입자가 접근할 경우 민감한 자격 정보가 노출될 위험도 있습니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 자세한 내용은 [설정 문서](/docs/master/configuration#environment-configuration)에서 확인하실 수 있습니다.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션 (Databases and Migrations)

이제 Laravel 애플리케이션을 만들었으니, 데이터를 데이터베이스에 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일에는 SQLite 데이터베이스를 사용하도록 되어 있습니다.

애플리케이션 생성 시, Laravel은 `database/database.sqlite` 파일을 자동으로 생성하고, 데이터베이스 테이블 구성을 위한 마이그레이션도 실행합니다.

MySQL이나 PostgreSQL과 같은 다른 데이터베이스 드라이버를 사용하려면, `.env` 설정 파일 내 데이터베이스 관련 값을 다음과 같이 수정할 수 있습니다:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

만약 SQLite 외의 데이터베이스를 사용하려면, 해당 데이터베이스를 직접 생성한 후 애플리케이션의 [데이터베이스 마이그레이션](/docs/master/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```

> [!NOTE]
> macOS 또는 Windows에서 MySQL, PostgreSQL, Redis를 로컬에 설치하려면 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/)을 사용하는 것도 좋은 방법입니다.

<a name="directory-configuration"></a>
### 디렉터리 구성 (Directory Configuration)

Laravel은 반드시 웹 서버에서 "웹 디렉터리"의 루트에서 서비스되어야 합니다. Laravel 애플리케이션을 "웹 디렉터리"의 하위 디렉터리에서 서비스 하려고 해서는 안 됩니다. 그렇게 하면 애플리케이션 내의 민감한 파일이 노출될 수 있습니다.

<a name="installation-using-herd"></a>
## Herd를 이용한 설치 (Installation Using Herd)

[Laravel Herd](https://herd.laravel.com)는 macOS와 Windows에서 사용 가능한 매우 빠르고 강력한 Laravel 및 PHP 개발 환경입니다. Herd는 PHP 및 Nginx 등 Laravel 개발을 시작하는 데 필요한 모든 것을 포함하고 있습니다.

Herd를 설치하면 바로 Laravel 개발을 시작할 수 있습니다. Herd에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm`, `nvm` 등 명령줄 도구가 포함되어 있습니다.

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans)는 Herd에 추가로 강력한 기능을 제공합니다. 예를 들어, 로컬 MySQL, Postgres, Redis 데이터베이스 생성 및 관리, 로컬 메일 보기, 로그 모니터링 등이 있습니다.

<a name="herd-on-macos"></a>
### macOS에서 Herd 사용 (Herd on macOS)

macOS에서 개발하는 경우 [Herd 웹사이트](https://herd.laravel.com)에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 PHP 버전을 자동으로 다운로드하고, Mac에서 [Nginx](https://www.nginx.com/)가 백그라운드에서 항상 실행되도록 설정합니다.

macOS용 Herd는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여 "주차(parked)" 디렉터리를 지원합니다. 주차된 디렉터리에 위치한 모든 Laravel 애플리케이션은 Herd에 의해 자동으로 서비스됩니다. 기본적으로 Herd는 `~/Herd`에 주차 디렉터리를 생성하며, 이 디렉터리 내의 Laravel 애플리케이션을 디렉터리명으로 `.test` 도메인에서 접속할 수 있습니다.

Herd 설치 후, 새로운 Laravel 애플리케이션을 생성하는 가장 빠른 방법은 Herd에 포함된 Laravel CLI를 사용하는 것입니다:

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

물론, Herd의 UI를 통해 주차 디렉터리 등 PHP 설정을 직접 관리할 수도 있습니다. Herd UI는 시스템 트레이에 있는 Herd 메뉴에서 열 수 있습니다.

자세한 내용은 [Herd 문서](https://herd.laravel.com/docs)를 참고하세요.

<a name="herd-on-windows"></a>
### Windows에서 Herd 사용 (Herd on Windows)

Windows용 Herd 설치 프로그램은 [Herd 웹사이트](https://herd.laravel.com/windows)에서 다운로드할 수 있습니다. 설치가 완료되면, Herd를 실행하여 온보딩 과정을 마치고 Herd UI에 처음 진입할 수 있습니다.

Herd UI는 시스템 트레이의 Herd 아이콘을 왼쪽 클릭하면 실행할 수 있습니다. 오른쪽 클릭하면 자주 사용하는 도구에 빠르게 접근할 수 있는 퀵 메뉴가 표시됩니다.

설치 과정에서 Herd는 홈 디렉터리 `%USERPROFILE%\Herd`에 "주차" 디렉터리를 생성합니다. 이 디렉터리 내에 위치한 모든 Laravel 애플리케이션은 자동으로 Herd에 의해 서비스되며, 해당 디렉터리명으로 `.test` 도메인에서 접속할 수 있습니다.

Herd 설치 후, 새로운 Laravel 애플리케이션을 만드는 가장 빠른 방법은 Herd에 포함된 Laravel CLI를 사용하는 것입니다. PowerShell을 열고 다음 명령어를 실행하세요:

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

자세한 내용은 [Windows용 Herd 문서](https://herd.laravel.com/docs/windows)에서 확인할 수 있습니다.

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션 개발 시 원하는 코드 에디터를 자유롭게 사용할 수 있습니다. 가볍고 확장성이 뛰어난 에디터를 원한다면, [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com)에 공식 [Laravel VS Code 익스텐션](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel)을 설치해 보세요. 구문 강조, 코드 스니펫, artisan 명령어 통합, Eloquent 모델·라우트·미들웨어·에셋·설정·Inertia.js에 대한 스마트 자동완성 등 강력한 라라벨 지원 기능을 제공합니다.

Laravel에 대한 강력하고 포괄적인 지원을 원한다면 JetBrains의 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025)을 살펴보세요. PhpStorm은 Blade 템플릿, Eloquent 모델·라우트·뷰·번역·컴포넌트에 대한 스마트 자동 완성, 프로젝트 간 코드 생성 및 내비게이션 등 라라벨 기능을 내장 지원합니다.

클라우드 기반 개발 환경을 원한다면, [Firebase Studio](https://firebase.studio/)를 이용하여 브라우저에서 바로 Laravel을 개발할 수 있습니다. 별도의 환경 세팅 없이 즉시 사용 가능하며, 어느 기기에서든 간편하게 Laravel 프로젝트를 시작할 수 있습니다.

<a name="laravel-and-ai"></a>
## 라라벨과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 간의 연계를 강화해주는 강력한 도구입니다. Boost는 AI 에이전트에게 Laravel에 특화된 컨텍스트와 도구, 지침을 제공하여, 버전에 맞는 정확한 코드와 Laravel 규칙을 준수하는 코드를 생성할 수 있게 해줍니다.

Boost를 애플리케이션에 설치하면, 에이전트는 15개 이상의 Laravel 특화 도구(패키지 탐지, 데이터베이스 쿼리, Laravel 문서 검색, 브라우저 로그 읽기, 테스트 생성, Tinker를 통한 코드 실행 등)에 접근할 수 있습니다.

또한 Boost는 설치된 패키지 버전에 맞춘 17,000건 이상의 벡터화된 Laravel 생태계 문서에 AI 에이전트가 접근할 수 있게 합니다. 이를 통해, 프로젝트에서 사용하는 정확한 버전에 대한 가이드와 조언을 얻을 수 있습니다.

Boost는 라라벨 프로젝트의 컨벤션을 따르는 AI 가이드라인도 제공하여, 에이전트가 규칙을 올바르게 따르고, 적절한 테스트를 작성하며, 자주 발생하는 실수를 방지할 수 있도록 돕습니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치 (Installing Laravel Boost)

Boost는 PHP 8.1 이상이 실행 중인 Laravel 10, 11, 12 애플리케이션에 설치할 수 있습니다. 다음과 같이 개발용 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치 후에는 인터랙티브 설치기를 실행합니다:

```shell
php artisan boost:install
```

설치기는 IDE 및 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 기능을 선택할 수 있도록 안내합니다. Boost는 기존 프로젝트 규칙을 존중하며, 기본적으로 강제적인 스타일 규칙을 적용하지 않습니다.

> [!NOTE]
> Boost에 대한 자세한 내용은 [Laravel Boost GitHub 저장소](https://github.com/laravel/boost)를 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
#### 커스텀 AI 가이드라인 추가

Laravel Boost에 직접 만든 AI 가이드라인을 추가하려면, 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. 이 파일들은 `boost:install` 실행 시 Boost의 기존 가이드라인과 함께 자동으로 포함됩니다.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

Laravel 애플리케이션을 만들었다면, 다음에 무엇을 학습해야 할지 궁금할 수 있습니다. 먼저 아래 문서를 읽고, Laravel이 어떻게 동작하는지 익혀보기를 강력히 권장합니다.

<div class="content-list" markdown="1">

- [요청 생명주기](/docs/master/lifecycle)
- [설정](/docs/master/configuration)
- [디렉터리 구조](/docs/master/structure)
- [프런트엔드](/docs/master/frontend)
- [서비스 컨테이너](/docs/master/container)
- [파사드](/docs/master/facades)

</div>

Laravel을 어떤 방식으로 사용할지에 따라서도 여러분의 다음 여정이 달라질 수 있습니다. Laravel 사용 방식에는 다양한 선택지가 있으며, 아래에서는 프레임워크의 주요 두 가지 사용 사례를 소개하겠습니다.

<a name="laravel-the-fullstack-framework"></a>
### 풀스택 프레임워크로서의 라라벨 (Laravel the Full Stack Framework)

Laravel은 풀스택 프레임워크로 사용할 수 있습니다. "풀스택" 프레임워크란, Laravel로 요청 라우트 처리와 [Blade 템플릿](/docs/master/blade) 또는 [Inertia](https://inertiajs.com)와 같은 단일 페이지 애플리케이션(하이브리드) 프런트엔드 랜더링까지 모두 맡기는 방식을 의미합니다. 이는 Laravel을 사용하는 가장 일반적이면서도 생산성이 뛰어난 개발 방식입니다.

이와 같은 방식으로 Laravel을 사용할 예정이라면, [프런트엔드 개발](/docs/master/frontend), [라우팅](/docs/master/routing), [뷰](/docs/master/views), [Eloquent ORM](/docs/master/eloquent) 등에 관한 공식 문서를 참고해보세요. 또한, [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지에도 관심을 가져볼 만 합니다. 이들 패키지는 Laravel을 풀스택 프레임워크로 활용하면서 최신 자바스크립트 애플리케이션의 UI 이점을 함께 누릴 수 있게 해줍니다.

풀스택 프레임워크로 Laravel을 쓴다면, [Vite](/docs/master/vite)를 이용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 꼭 익혀두길 권장합니다.

> [!NOTE]
> 애플리케이션 개발을 좀 더 빠르게 시작하고자 한다면, 공식 [애플리케이션 스타터 키트](/docs/master/starter-kits)를 활용해보세요.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 라라벨 (Laravel the API Backend)

Laravel은 자바스크립트 기반의 단일 페이지 앱(SPA)이나 모바일 앱의 API 백엔드로도 사용할 수 있습니다. 예를 들어, [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수도 있습니다. 이 경우 Laravel을 통해 [인증](/docs/master/sanctum), 데이터 저장과 조회 기능을 제공하며, 큐, 이메일, 알림 등 강력한 서비스도 함께 활용할 수 있습니다.

이런 방식을 선택한다면, [라우팅](/docs/master/routing), [Laravel Sanctum](/docs/master/sanctum), [Eloquent ORM](/docs/master/eloquent) 문서를 참고해 보세요.