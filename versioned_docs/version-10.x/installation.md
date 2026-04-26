---
slug: /
---

# 설치 (Installation)

- [Laravel 만나보기](#meet-laravel)
    - [왜 Laravel인가요?](#why-laravel)
- [Laravel 프로젝트 생성](#creating-a-laravel-project)
- [초기 설정](#initial-configuration)
    - [환경 기반 설정](#environment-based-configuration)
    - [데이터베이스와 마이그레이션](#databases-and-migrations)
    - [디렉터리 설정](#directory-configuration)
- [Sail을 사용한 Docker 설치](#docker-installation-using-sail)
    - [macOS에서 Sail 사용](#sail-on-macos)
    - [Windows에서 Sail 사용](#sail-on-windows)
    - [Linux에서 Sail 사용](#sail-on-linux)
    - [Sail 서비스 선택](#choosing-your-sail-services)
- [IDE 지원](#ide-support)
- [Laravel과 AI](#laravel-and-ai)
    - [Laravel Boost 설치](#installing-laravel-boost)
- [다음 단계](#next-steps)
    - [풀스택 프레임워크로서의 Laravel](#laravel-the-fullstack-framework)
    - [API 백엔드로서의 Laravel](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Laravel 만나보기 (Meet Laravel)

Laravel은 표현력이 뛰어나고 우아한 문법을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션을 만들기 위한 구조와 출발점을 제공하므로, 세부적인 부분은 프레임워크에 맡기고 여러분은 멋진 것을 만드는 데 집중할 수 있습니다.

Laravel은 철저한 의존성 주입, 표현력 있는 데이터베이스 추상화 계층, 큐와 예약 작업, 단위 및 통합 테스트 등 강력한 기능을 제공하면서도 뛰어난 개발자 경험을 제공하기 위해 노력합니다.

PHP 웹 프레임워크가 처음이든, 수년간의 경험이 있든, Laravel은 여러분과 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서 첫걸음을 내딛는 데 도움을 주거나, 전문성을 한 단계 더 끌어올릴 수 있도록 도와드리겠습니다. 여러분이 무엇을 만들어낼지 기대됩니다.

> [!NOTE]
> Laravel이 처음이신가요? 첫 Laravel 애플리케이션을 만드는 과정을 함께 따라가며 프레임워크를 직접 익힐 수 있는 [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인해 보세요.

<a name="why-laravel"></a>
### 왜 Laravel인가요?

웹 애플리케이션을 만들 때 사용할 수 있는 도구와 프레임워크는 다양합니다. 하지만 우리는 Laravel이 현대적인 풀스택 웹 애플리케이션을 만드는 데 가장 좋은 선택이라고 믿습니다.

#### 점진적으로 성장하는 프레임워크

우리는 Laravel을 "점진적" 프레임워크라고 부릅니다. 이는 Laravel이 여러분과 함께 성장한다는 뜻입니다. 이제 막 웹 개발을 시작했다면, Laravel의 방대한 문서, 가이드, [동영상 튜토리얼](https://laracasts.com)이 부담 없이 기본기를 익히는 데 도움을 줄 것입니다.

숙련된 개발자라면 Laravel은 [의존성 주입](/docs/10.x/container), [단위 테스트](/docs/10.x/testing), [큐](/docs/10.x/queues), [실시간 이벤트](/docs/10.x/broadcasting) 등을 위한 견고한 도구를 제공합니다. Laravel은 전문적인 웹 애플리케이션 구축에 맞게 세심하게 조정되어 있으며, 엔터프라이즈 워크로드를 처리할 준비가 되어 있습니다.

#### 확장 가능한 프레임워크

Laravel은 매우 뛰어난 확장성을 제공합니다. PHP의 확장 친화적인 특성과 Redis 같은 빠른 분산 캐시 시스템에 대한 Laravel의 기본 지원 덕분에, Laravel로 수평 확장을 하는 일은 매우 쉽습니다. 실제로 Laravel 애플리케이션은 매월 수억 건의 요청을 처리하도록 손쉽게 확장된 사례가 있습니다.

극단적인 확장이 필요하신가요? [Laravel Vapor](https://vapor.laravel.com) 같은 플랫폼을 사용하면 AWS의 최신 서버리스 기술 위에서 Laravel 애플리케이션을 거의 무제한에 가까운 규모로 실행할 수 있습니다.

#### 커뮤니티 프레임워크

Laravel은 PHP 생태계의 최고의 패키지들을 결합하여 가장 견고하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 뛰어난 개발자들이 [프레임워크에 기여](https://github.com/laravel/framework)해 왔습니다. 어쩌면 여러분도 Laravel 기여자가 될 수 있습니다.

<a name="creating-a-laravel-project"></a>
## Laravel 프로젝트 생성 (Creating a Laravel Project)

첫 Laravel 프로젝트를 만들기 전에 로컬 머신에 PHP와 [Composer](https://getcomposer.org)가 설치되어 있는지 확인하세요. macOS에서 개발 중이라면 [Laravel Herd](https://herd.laravel.com)를 통해 몇 분 안에 PHP와 Composer를 설치할 수 있습니다. 또한 [Node와 NPM 설치](https://nodejs.org)를 권장합니다.

PHP와 Composer를 설치한 뒤에는 Composer의 `create-project` 명령어를 사용하여 새 Laravel 프로젝트를 만들 수 있습니다.

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

또는 Composer를 통해 [Laravel installer](https://github.com/laravel/installer)를 전역으로 설치하여 새 Laravel 프로젝트를 만들 수도 있습니다.

```nothing
composer global require laravel/installer

laravel new example-app
```

프로젝트가 생성되면 Laravel Artisan의 `serve` 명령어를 사용하여 Laravel 로컬 개발 서버를 시작하세요.

```nothing
cd example-app

php artisan serve
```

Artisan 개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접근할 수 있습니다. 이제 [Laravel 생태계에서 다음 단계로 나아갈 준비](#next-steps)가 되었습니다. 물론 [데이터베이스를 설정](#databases-and-migrations)하고 싶을 수도 있습니다.

> [!NOTE]
> Laravel 애플리케이션 개발을 더 빠르게 시작하고 싶다면 [스타터 키트](/docs/10.x/starter-kits) 중 하나를 사용하는 것을 고려해 보세요. Laravel 스타터 키트는 새 Laravel 애플리케이션을 위한 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

<a name="initial-configuration"></a>
## 초기 설정 (Initial Configuration)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 문서가 작성되어 있으므로, 파일을 살펴보며 사용할 수 있는 옵션에 익숙해져도 좋습니다.

Laravel은 기본 상태에서 추가 설정이 거의 필요하지 않습니다. 바로 개발을 시작해도 됩니다. 하지만 `config/app.php` 파일과 그 문서를 검토해 보는 것이 좋습니다. 이 파일에는 애플리케이션에 맞게 변경하고 싶을 수 있는 `timezone`, `locale` 같은 여러 옵션이 포함되어 있습니다.

<a name="environment-based-configuration"></a>
### 환경 기반 설정

Laravel의 많은 설정 옵션 값은 애플리케이션이 로컬 머신에서 실행되는지, 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있습니다. 그래서 중요한 설정 값 다수는 애플리케이션 루트에 있는 `.env` 파일을 사용하여 정의됩니다.

`.env` 파일은 애플리케이션의 소스 관리에 커밋해서는 안 됩니다. 애플리케이션을 사용하는 각 개발자/서버마다 서로 다른 환경 설정이 필요할 수 있기 때문입니다. 더 나아가 침입자가 소스 관리 저장소에 접근하게 되면 민감한 인증 정보가 노출될 수 있으므로 보안 위험이 됩니다.

> [!NOTE]
> `.env` 파일과 환경 기반 설정에 대한 자세한 내용은 전체 [설정 문서](/docs/10.x/configuration#environment-configuration)를 확인하세요.

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션

이제 Laravel 애플리케이션을 만들었으므로, 아마 데이터베이스에 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 설정 파일은 Laravel이 MySQL 데이터베이스와 상호작용하며 `127.0.0.1`에서 데이터베이스에 접근하도록 지정합니다.

> [!NOTE]
> macOS에서 개발 중이고 MySQL, Postgres, Redis를 로컬에 설치해야 한다면 [DBngin](https://dbngin.com/) 사용을 고려해 보세요.

로컬 머신에 MySQL이나 Postgres를 설치하고 싶지 않다면 언제든지 [SQLite](https://www.sqlite.org/index.html) 데이터베이스를 사용할 수 있습니다. SQLite는 작고 빠르며 자체 완결적인 데이터베이스 엔진입니다. 시작하려면 `.env` 설정 파일을 업데이트하여 Laravel의 `sqlite` 데이터베이스 드라이버를 사용하도록 변경하세요. 다른 데이터베이스 설정 옵션은 제거해도 됩니다.

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

SQLite 데이터베이스를 설정한 뒤에는 애플리케이션의 [데이터베이스 마이그레이션](/docs/10.x/migrations)을 실행할 수 있습니다. 이 작업은 애플리케이션의 데이터베이스 테이블을 생성합니다.

```shell
php artisan migrate
```

애플리케이션을 위한 SQLite 데이터베이스가 존재하지 않는 경우, Laravel은 데이터베이스를 생성할지 물어봅니다. 일반적으로 SQLite 데이터베이스 파일은 `database/database.sqlite`에 생성됩니다.

<a name="directory-configuration"></a>
### 디렉터리 설정

Laravel은 항상 웹 서버에 설정된 "웹 디렉터리"의 루트에서 제공되어야 합니다. "웹 디렉터리"의 하위 디렉터리에서 Laravel 애플리케이션을 제공하려고 시도해서는 안 됩니다. 그렇게 하면 애플리케이션 내부의 민감한 파일이 노출될 수 있습니다.

<a name="docker-installation-using-sail"></a>
## Sail을 사용한 Docker 설치 (Docker Installation Using Sail)

우리는 사용자가 선호하는 운영체제와 관계없이 Laravel을 가능한 한 쉽게 시작할 수 있기를 바랍니다. 그래서 로컬 머신에서 Laravel 프로젝트를 개발하고 실행하는 방법에는 여러 가지 선택지가 있습니다. 이러한 선택지는 나중에 살펴봐도 되지만, Laravel은 [Docker](https://www.docker.com)를 사용하여 Laravel 프로젝트를 실행할 수 있는 내장 솔루션인 [Sail](/docs/10.x/sail)을 제공합니다.

Docker는 애플리케이션과 서비스를 작고 가벼운 "컨테이너" 안에서 실행하는 도구입니다. 이 컨테이너는 로컬 머신에 설치된 소프트웨어나 설정에 영향을 주지 않습니다. 즉, 웹 서버나 데이터베이스 같은 복잡한 개발 도구를 로컬 머신에 설정하거나 구성하는 일을 걱정하지 않아도 됩니다. 시작하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop)만 설치하면 됩니다.

Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 가벼운 명령줄 인터페이스입니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 사용하여 Laravel 애플리케이션을 구축할 수 있는 훌륭한 출발점을 제공합니다.

> [!NOTE]
> 이미 Docker 전문가이신가요? 걱정하지 마세요! Sail의 모든 것은 Laravel에 포함된 `docker-compose.yml` 파일을 사용하여 커스터마이즈할 수 있습니다.

<a name="sail-on-macos"></a>
### macOS에서 Sail 사용

Mac에서 개발 중이고 [Docker Desktop](https://www.docker.com/products/docker-desktop)이 이미 설치되어 있다면, 간단한 터미널 명령어로 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하면 됩니다.

```shell
curl -s "https://laravel.build/example-app" | bash
```

물론 이 URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름에는 영숫자, 하이픈, 밑줄만 포함되어야 합니다. Laravel 애플리케이션의 디렉터리는 명령어를 실행한 디렉터리 안에 생성됩니다.

Sail 애플리케이션 컨테이너가 로컬 머신에서 빌드되는 동안 Sail 설치에는 몇 분이 걸릴 수 있습니다.

프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 간단한 명령줄 인터페이스를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 애플리케이션에 접근할 수 있습니다: http://localhost.

> [!NOTE]
> Laravel Sail에 대해 더 알아보려면 [전체 문서](/docs/10.x/sail)를 확인하세요.

<a name="sail-on-windows"></a>
### Windows에서 Sail 사용

Windows 머신에서 새 Laravel 애플리케이션을 만들기 전에 [Docker Desktop](https://www.docker.com/products/docker-desktop)을 설치했는지 확인하세요. 다음으로 Windows Subsystem for Linux 2(WSL2)가 설치되어 있고 활성화되어 있는지 확인해야 합니다. WSL을 사용하면 Windows 10에서 Linux 바이너리 실행 파일을 네이티브로 실행할 수 있습니다. WSL2 설치 및 활성화 방법에 대한 정보는 Microsoft의 [개발자 환경 문서](https://docs.microsoft.com/en-us/windows/wsl/install-win10)에서 확인할 수 있습니다.

> [!NOTE]
> WSL2를 설치하고 활성화한 뒤에는 Docker Desktop이 [WSL2 백엔드를 사용하도록 설정](https://docs.docker.com/docker-for-windows/wsl/)되어 있는지 확인해야 합니다.

이제 첫 Laravel 프로젝트를 만들 준비가 되었습니다. [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)을 실행하고 WSL2 Linux 운영체제용 새 터미널 세션을 시작하세요. 그런 다음 간단한 터미널 명령어를 사용하여 새 Laravel 프로젝트를 만들 수 있습니다. 예를 들어 "example-app"이라는 디렉터리에 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하면 됩니다.

```shell
curl -s https://laravel.build/example-app | bash
```

물론 이 URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름에는 영숫자, 하이픈, 밑줄만 포함되어야 합니다. Laravel 애플리케이션의 디렉터리는 명령어를 실행한 디렉터리 안에 생성됩니다.

Sail 애플리케이션 컨테이너가 로컬 머신에서 빌드되는 동안 Sail 설치에는 몇 분이 걸릴 수 있습니다.

프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 간단한 명령줄 인터페이스를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 애플리케이션에 접근할 수 있습니다: http://localhost.

> [!NOTE]
> Laravel Sail에 대해 더 알아보려면 [전체 문서](/docs/10.x/sail)를 확인하세요.

#### WSL2 내에서 개발하기

물론 WSL2 설치 환경 안에 생성된 Laravel 애플리케이션 파일을 수정할 수 있어야 합니다. 이를 위해 Microsoft의 [Visual Studio Code](https://code.visualstudio.com) 편집기와 Microsoft에서 제공하는 [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 확장 프로그램 사용을 권장합니다.

이 도구들이 설치되면 Windows Terminal에서 애플리케이션의 루트 디렉터리로 이동한 뒤 `code .` 명령어를 실행하여 어떤 Laravel 프로젝트든 열 수 있습니다.

<a name="sail-on-linux"></a>
### Linux에서 Sail 사용

Linux에서 개발 중이고 [Docker Compose](https://docs.docker.com/compose/install/)가 이미 설치되어 있다면, 간단한 터미널 명령어로 새 Laravel 프로젝트를 만들 수 있습니다.

먼저 Linux용 Docker Desktop을 사용 중이라면 다음 명령어를 실행해야 합니다. Linux용 Docker Desktop을 사용하지 않는다면 이 단계는 건너뛰어도 됩니다.

```shell
docker context use default
```

그런 다음 "example-app"이라는 디렉터리에 새 Laravel 애플리케이션을 만들려면 터미널에서 다음 명령어를 실행하면 됩니다.

```shell
curl -s https://laravel.build/example-app | bash
```

물론 이 URL의 "example-app"은 원하는 이름으로 변경할 수 있습니다. 단, 애플리케이션 이름에는 영숫자, 하이픈, 밑줄만 포함되어야 합니다. Laravel 애플리케이션의 디렉터리는 명령어를 실행한 디렉터리 안에 생성됩니다.

Sail 애플리케이션 컨테이너가 로컬 머신에서 빌드되는 동안 Sail 설치에는 몇 분이 걸릴 수 있습니다.

프로젝트가 생성되면 애플리케이션 디렉터리로 이동하여 Laravel Sail을 시작할 수 있습니다. Laravel Sail은 Laravel의 기본 Docker 설정과 상호작용하기 위한 간단한 명령줄 인터페이스를 제공합니다.

```shell
cd example-app

./vendor/bin/sail up
```

애플리케이션의 Docker 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 애플리케이션에 접근할 수 있습니다: http://localhost.

> [!NOTE]
> Laravel Sail에 대해 더 알아보려면 [전체 문서](/docs/10.x/sail)를 확인하세요.

<a name="choosing-your-sail-services"></a>
### Sail 서비스 선택

Sail을 통해 새 Laravel 애플리케이션을 만들 때 `with` 쿼리 문자열 변수를 사용하여 새 애플리케이션의 `docker-compose.yml` 파일에 어떤 서비스를 설정할지 선택할 수 있습니다. 사용 가능한 서비스에는 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, `mailpit`이 포함됩니다.
```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

구성하려는 서비스를 지정하지 않으면 `mysql`, `redis`, `meilisearch`, `mailpit`, `selenium`으로 구성된 기본 스택이 설정됩니다.

URL에 `devcontainer` 매개변수를 추가하여 Sail이 기본 [Devcontainer](/docs/10.x/sail#using-devcontainers)를 설치하도록 지시할 수 있습니다.

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
## IDE 지원 (IDE Support)

Laravel 애플리케이션을 개발할 때 원하는 코드 편집기를 자유롭게 사용할 수 있습니다. 하지만 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/)은 [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html)를 포함하여 Laravel과 그 생태계를 폭넓게 지원합니다.

또한 커뮤니티에서 유지 관리하는 [Laravel Idea](https://laravel-idea.com/) PhpStorm 플러그인은 코드 생성, Eloquent 문법 자동 완성, 유효성 검증 규칙 자동 완성 등 다양한 유용한 IDE 확장 기능을 제공합니다.

<a name="laravel-and-ai"></a>
## Laravel과 AI (Laravel and AI)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 간극을 메워 주는 강력한 도구입니다. Boost는 AI 에이전트에 Laravel 전용 컨텍스트, 도구, 지침을 제공하여 Laravel 규칙을 따르는 더 정확하고 버전별로 알맞은 코드를 생성할 수 있게 합니다.

Laravel 애플리케이션에 Boost를 설치하면 AI 에이전트는 사용 중인 패키지를 파악하고, 데이터베이스를 쿼리하고, Laravel 문서를 검색하고, 브라우저 로그를 읽고, 테스트를 생성하고, Tinker를 통해 코드를 실행하는 기능을 포함한 15개 이상의 전문 도구에 접근할 수 있습니다.

또한 Boost는 설치된 패키지 버전에 맞춘 17,000개 이상의 벡터화된 Laravel 생태계 문서를 AI 에이전트에 제공합니다. 즉, 에이전트는 프로젝트에서 사용하는 정확한 버전에 맞는 안내를 제공할 수 있습니다.

Boost에는 Laravel에서 유지 관리하는 AI 지침도 포함되어 있어, 에이전트가 Laravel 코드를 생성할 때 프레임워크 규칙을 따르고, 적절한 테스트를 작성하며, 흔한 실수를 피하도록 도와줍니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치

Boost는 PHP 8.1 이상에서 실행되는 Laravel 10, 11, 12 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치합니다.

```shell
composer require laravel/boost --dev
```

설치가 끝나면 대화형 설치 프로그램을 실행합니다.

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 적합한 기능을 선택할 수 있게 합니다. Boost는 기존 프로젝트 규칙을 존중하며, 기본적으로 특정 스타일 규칙을 강제로 적용하지 않습니다.

> [!NOTE]
> Boost에 대해 더 자세히 알아보려면 [GitHub의 Laravel Boost 저장소](https://github.com/laravel/boost)를 확인하십시오.

<a name="next-steps"></a>
## 다음 단계 (Next Steps)

이제 Laravel 프로젝트를 만들었으므로 다음에 무엇을 배워야 할지 궁금할 수 있습니다. 먼저 다음 문서를 읽으며 Laravel이 어떻게 작동하는지 익히는 것을 강력히 권장합니다.

<div class="content-list" markdown="1">

- [요청 라이프사이클](/docs/10.x/lifecycle)
- [설정](/docs/10.x/configuration)
- [디렉터리 구조](/docs/10.x/structure)
- [프론트엔드](/docs/10.x/frontend)
- [서비스 컨테이너](/docs/10.x/container)
- [파사드](/docs/10.x/facades)

</div>

Laravel을 어떤 방식으로 사용하려는지에 따라 다음 단계도 달라집니다. Laravel을 사용하는 방법은 다양하며, 아래에서는 이 프레임워크의 두 가지 주요 사용 사례를 살펴보겠습니다.

> [!NOTE]
> Laravel이 처음이신가요? 첫 Laravel 애플리케이션을 만드는 과정을 함께 따라가며 프레임워크를 직접 익힐 수 있는 [Laravel Bootcamp](https://bootcamp.laravel.com)를 확인하십시오.

<a name="laravel-the-fullstack-framework"></a>
### 풀 스택 프레임워크로서의 Laravel

Laravel은 풀 스택 프레임워크로 사용할 수 있습니다. 여기서 "풀 스택" 프레임워크란 Laravel을 사용해 애플리케이션으로 들어오는 요청을 라우팅하고, [Blade 템플릿](/docs/10.x/blade) 또는 [Inertia](https://inertiajs.com)와 같은 단일 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드를 렌더링한다는 의미입니다. 이는 Laravel 프레임워크를 사용하는 가장 일반적인 방식이며, 저희가 생각하기에 Laravel을 가장 생산적으로 사용하는 방식입니다.

Laravel을 이런 방식으로 사용할 계획이라면 [프론트엔드 개발](/docs/10.x/frontend), [라우팅](/docs/10.x/routing), [뷰](/docs/10.x/views), [Eloquent ORM](/docs/10.x/eloquent)에 관한 문서를 확인해 보십시오. 또한 [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 같은 커뮤니티 패키지를 배우는 것도 도움이 될 수 있습니다. 이러한 패키지를 사용하면 단일 페이지 JavaScript 애플리케이션이 제공하는 다양한 UI 장점을 누리면서도 Laravel을 풀 스택 프레임워크로 사용할 수 있습니다.

Laravel을 풀 스택 프레임워크로 사용한다면 [Vite](/docs/10.x/vite)를 사용해 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법도 반드시 익히는 것이 좋습니다.

> [!NOTE]
> 애플리케이션 개발을 빠르게 시작하고 싶다면 공식 [애플리케이션 스타터 키트](/docs/10.x/starter-kits) 중 하나를 확인하십시오.

<a name="laravel-the-api-backend"></a>
### API 백엔드로서의 Laravel

Laravel은 JavaScript 단일 페이지 애플리케이션이나 모바일 애플리케이션을 위한 API 백엔드로도 사용할 수 있습니다. 예를 들어 [Next.js](https://nextjs.org) 애플리케이션의 API 백엔드로 Laravel을 사용할 수 있습니다. 이 경우 Laravel을 사용해 애플리케이션에 [인증](/docs/10.x/sanctum)과 데이터 저장 및 조회 기능을 제공하면서, 큐, 이메일, 알림 등 Laravel의 강력한 서비스도 함께 활용할 수 있습니다.

Laravel을 이런 방식으로 사용할 계획이라면 [라우팅](/docs/10.x/routing), [Laravel Sanctum](/docs/10.x/sanctum), [Eloquent ORM](/docs/10.x/eloquent)에 관한 문서를 확인해 보십시오.

> [!NOTE]
> Laravel 백엔드와 Next.js 프론트엔드의 스캐폴딩을 빠르게 시작해야 하나요? Laravel Breeze는 [API 스택](/docs/10.x/starter-kits#breeze-and-next)과 [Next.js 프론트엔드 구현](https://github.com/laravel/breeze-next)을 제공하므로 몇 분 안에 시작할 수 있습니다.
