# 업그레이드 가이드 (Upgrade Guide)

- [11.x에서 12.0으로 업그레이드](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 영향도가 큰 변경 사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel Installer 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 영향도가 중간인 변경 사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 영향도가 낮은 변경 사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Concurrency 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해결](#container-class-dependency-resolution)
- [이미지 유효성 검증에서 SVG 제외](#image-validation)
- [로컬 파일시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [멀티 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 시간: 5분

> [!NOTE]
> 가능한 모든 호환성 깨짐 변경 사항(breaking change)을 문서화하려고 노력합니다. 다만 일부 변경 사항은 프레임워크의 잘 사용되지 않는 영역에 존재하므로 실제로 애플리케이션에 영향을 주는 경우는 일부에 불과할 수 있습니다. 시간을 절약하고 싶다면 애플리케이션 업그레이드를 자동화하는 데 도움을 주는 [Laravel Shift](https://laravelshift.com/)를 사용할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework` → `^12.0`
- `phpunit/phpunit` → `^11.0`
- `pestphp/pest` → `^3.0`

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

Carbon 2.x 지원이 제거되었습니다. 이제 모든 Laravel 12 애플리케이션은 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)를 사용해야 합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel Installer 업데이트

새로운 Laravel 애플리케이션을 생성할 때 Laravel installer CLI 도구를 사용한다면, Laravel 12.x 및 [새로운 Laravel starter kits](https://laravel.com/starter-kits)와 호환되도록 installer를 업데이트해야 합니다.

만약 `composer global require`를 통해 Laravel installer를 설치했다면 다음 명령어로 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

만약 처음에 `php.new`를 통해 PHP와 Laravel을 설치했다면, 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 PHP와 Laravel installer를 설치할 수 있습니다.

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

또는 [Laravel Herd](https://herd.laravel.com)에 포함된 Laravel installer를 사용 중이라면 Herd를 최신 버전으로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자에서 `$expires` 매개변수는 이제 **분(minutes)** 이 아니라 **초(seconds)** 단위로 전달해야 합니다.

<a name="concurrency"></a>
### Concurrency

<a name="concurrency-result-index-mapping"></a>
#### Concurrency 결과 인덱스 매핑

**영향 가능성: 낮음**

연관 배열(associative array)을 사용하여 `Concurrency::run` 메서드를 호출할 경우, 이제 병렬 작업의 결과가 해당 키와 함께 반환됩니다.

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
### 컨테이너 (Container)

<a name="container-class-dependency-resolution"></a>
#### 컨테이너 클래스 의존성 해결

**영향 가능성: 낮음**

의존성 주입 컨테이너(dependency injection container)는 이제 클래스 인스턴스를 생성할 때 **클래스 속성의 기본값(default value)** 을 존중합니다.

이전에 컨테이너가 기본값을 무시하고 인스턴스를 생성하는 동작에 의존하고 있었다면, 애플리케이션을 이 새로운 동작에 맞게 수정해야 할 수 있습니다.

```php
class Example
{
    public function __construct(public ?Carbon $date = null) {}
}

$example = resolve(Example::class);

// <= 11.x
$example->date instanceof Carbon;

// >= 12.x
$example->date === null;
```

<a name="database"></a>
### 데이터베이스 (Database)

<a name="multi-schema-database-inspecting"></a>
#### 멀티 스키마 데이터베이스 검사

**영향 가능성: 낮음**

이제 `Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 기본적으로 **모든 스키마의 결과를 포함**합니다.

특정 스키마의 결과만 가져오려면 `schema` 인수를 전달할 수 있습니다.

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: 'main');

// 'main'과 'blog' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 **스키마가 포함된 테이블 이름**을 반환합니다. 원하는 동작에 맞게 `schemaQualified` 인수를 사용할 수 있습니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

또한 `db:table` 및 `db:show` 명령어는 이제 PostgreSQL과 SQL Server처럼 MySQL, MariaDB, SQLite에서도 **모든 스키마의 결과를 출력**합니다.

<a name="database-constructor-signature-changes"></a>
#### Database 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

Laravel 12에서는 몇몇 저수준 데이터베이스 클래스의 생성자가 이제 `Illuminate\Database\Connection` 인스턴스를 필요로 합니다.

**이 변경 사항은 주로 데이터베이스 패키지를 유지보수하는 개발자에게 적용됩니다. 일반적인 애플리케이션 개발에는 영향을 줄 가능성이 매우 낮습니다.**

`Illuminate\Database\Schema\Blueprint`

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Connection` 인스턴스를 요구합니다. 이는 주로 `Blueprint` 인스턴스를 직접 생성하는 애플리케이션이나 패키지에 영향을 줍니다.

`Illuminate\Database\Grammar`

`Illuminate\Database\Grammar` 클래스의 생성자 역시 이제 `Connection` 인스턴스를 필요로 합니다. 이전 버전에서는 생성 이후 `setConnection()` 메서드를 통해 연결을 설정했습니다. 이 메서드는 Laravel 12에서 제거되었습니다.

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
```

또한 다음 API는 제거되었거나 더 이상 사용이 권장되지 않습니다(deprecated).

<div class="content-list" markdown="1">

- `Blueprint::getPrefix()` 메서드는 deprecated 되었습니다.
- `Connection::withTablePrefix()` 메서드는 제거되었습니다.
- `Grammar::getTablePrefix()` 및 `setTablePrefix()` 메서드는 deprecated 되었습니다.
- `Grammar::setConnection()` 메서드는 제거되었습니다.

</div>

테이블 prefix를 다룰 때는 이제 데이터베이스 연결에서 직접 가져와야 합니다.

```php
$prefix = $connection->getTablePrefix();
```

만약 커스텀 데이터베이스 드라이버, 스키마 빌더, 또는 grammar 구현을 유지보수하고 있다면, 생성자를 검토하여 `Connection` 인스턴스를 전달하도록 해야 합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7

**영향 가능성: 중간**

`HasUuids` trait은 이제 **UUID 스펙의 버전 7(UUIDv7, ordered UUID)** 과 호환되는 UUID를 반환합니다.

만약 모델 ID에 대해 기존처럼 **ordered UUIDv4 문자열**을 계속 사용하고 싶다면 `HasVersion4Uuids` trait을 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` trait은 제거되었습니다. 이전에 이 trait을 사용하고 있었다면 이제 동일한 동작을 제공하는 `HasUuids` trait을 사용하면 됩니다.

<a name="requests"></a>
### Requests

<a name="nested-array-request-merging"></a>
#### 중첩 배열 Request 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 **dot 표기법(dot notation)** 을 사용하여 중첩 배열 데이터를 병합할 수 있습니다.

이전에 dot 표기법을 **최상위 배열 키(top-level key)** 로 생성하는 동작에 의존하고 있었다면, 새로운 동작에 맞게 애플리케이션을 수정해야 할 수 있습니다.

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="routing"></a>
### 라우팅 (Routing)

<a name="route-precedence"></a>
#### 라우트 우선순위

**영향 가능성: 낮음**

같은 이름을 가진 여러 라우트가 있을 때의 라우팅 동작이 **캐시된 라우팅과 캐시되지 않은 라우팅 사이에서 동일하게 동작하도록 통일**되었습니다.

이제 캐시되지 않은 라우팅에서도 **마지막으로 등록된 라우트가 아니라, 처음 등록된 라우트**가 매칭됩니다.

<a name="storage"></a>
### 스토리지 (Storage)

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일시스템 디스크 기본 루트 경로

**영향 가능성: 낮음**

애플리케이션의 filesystems 설정에서 `local` 디스크를 명시적으로 정의하지 않은 경우, 이제 Laravel은 기본적으로 `storage/app/private` 경로를 루트로 사용합니다.

이전 버전에서는 기본값이 `storage/app` 이었습니다.

따라서 별도 설정이 없다면 `Storage::disk('local')` 호출은 이제 `storage/app/private` 경로에서 파일을 읽고 쓰게 됩니다.

이전 동작을 유지하려면 `local` 디스크를 수동으로 정의하고 원하는 루트 경로를 설정해야 합니다.

<a name="validation"></a>
### 유효성 검증 (Validation)

<a name="image-validation"></a>
#### 이미지 유효성 검증에서 SVG 제외

**영향 가능성: 낮음**

`image` 유효성 검증 규칙은 이제 기본적으로 **SVG 이미지를 허용하지 않습니다**.

`image` 규칙을 사용할 때 SVG를 허용하려면 명시적으로 설정해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// Or...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타 (Miscellaneous)

또한 `laravel/laravel`의 변경 사항을 [GitHub repository](https://github.com/laravel/laravel)에서 확인하는 것을 권장합니다.

이 변경 사항 중 많은 것들은 필수는 아니지만 애플리케이션과 동기화해 두는 것이 좋을 수 있습니다. 일부 변경 사항은 이 업그레이드 가이드에서 다루지만, 설정 파일 변경이나 주석 수정과 같은 일부 변경 사항은 포함되지 않을 수 있습니다.

[GitHub comparison tool](https://github.com/laravel/laravel/compare/11.x...12.x)을 사용하면 변경된 내용을 쉽게 확인하고, 애플리케이션에 필요한 업데이트만 선택하여 적용할 수 있습니다.