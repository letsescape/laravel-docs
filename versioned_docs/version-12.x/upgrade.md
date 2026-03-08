# 업그레이드 가이드 (Upgrade Guide)

- [12.0으로 업그레이드하기 (11.x → 12.0)](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 주요 변경 사항 (High Impact Changes)

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 중간 영향도 변경 사항 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 낮은 영향도 변경 사항 (Low Impact Changes)

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해석](#container-class-dependency-resolution)
- [SVG가 제외된 이미지 유효성 검증](#image-validation)
- [로컬 파일시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [멀티 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드하기 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 소요 시간: 5분

> [!NOTE]
> 가능한 모든 변경 사항(브레이킹 체인지)을 문서화하려고 하였습니다. 일부 변경 사항은 프레임워크의 생소한 부분에 해당하므로, 실제로는 일부만이 여러분의 애플리케이션에 영향을 줄 수 있습니다. 시간을 아끼고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용해 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트 (Updating Dependencies)

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 반드시 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`을 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

Carbon 2.x 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 반드시 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)를 필요로 합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel 인스톨러 업데이트 (Updating the Laravel Installer)

Laravel 인스톨러 CLI 도구를 사용해 새로운 Laravel 애플리케이션을 생성하고 있다면, 인스톨러 설치본을 Laravel 12.x 및 [새로운 Laravel 스타터 키트](https://laravel.com/starter-kits)와 호환되도록 업데이트해야 합니다. 만약 `composer global require` 명령어로 Laravel 인스톨러를 설치했다면, 아래 명령어로 인스톨러를 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

만약 `php.new`를 통해 PHP와 Laravel을 처음 설치했다면, 해당 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행해 최신 PHP와 Laravel 인스톨러를 설치하면 됩니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행하세요...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는, [Laravel Herd](https://herd.laravel.com)의 번들로 포함된 인스톨러를 사용 중이라면, Herd 설치본을 최신 릴리즈로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증 (Authentication)

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자에서 `$expires` 파라미터는 이제 분(minute) 단위가 아닌 **초(second)** 단위로 입력해야 합니다.

<a name="concurrency"></a>
### 동시성 (Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑 (Concurrency Result Index Mapping)

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열(associative array)로 호출할 때, 이제 각 작업의 결과가 해당 키와 함께 반환됩니다:

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
#### 컨테이너 클래스 의존성 해석 (Container Class Dependency Resolution)

**영향 가능성: 낮음**

의존성 주입 컨테이너는 이제 클래스 속성의 기본값(default value)을 존중하여 클래스 인스턴스를 해석합니다. 이전에 컨테이너가 기본값 없이 인스턴스를 반환하길 기대했다면, 이 변경 사항에 맞게 애플리케이션 코드를 조정해야 할 수 있습니다:

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
#### 멀티 스키마 데이터베이스 검사 (Multi-Schema Database Inspecting)

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드가 이제 기본적으로 **모든 스키마의 결과**를 반환합니다. 특정 스키마만 조회하려면 `schema` 인수를 전달할 수 있습니다:

```php
// 모든 스키마의 테이블 가져오기...
$tables = Schema::getTables();

// 'main' 스키마의 테이블만 가져오기...
$tables = Schema::getTables(schema: 'main');

// 'main', 'blog' 스키마의 테이블 가져오기...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 **스키마가 포함된 테이블명(schema-qualified table names)** 을 반환합니다. 반환 형식을 바꾸려면 `schemaQualified` 인수를 전달할 수 있습니다:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령어도 이제 MySQL, MariaDB, SQLite에서 PostgreSQL과 SQL Server와 동일하게 모든 스키마의 결과를 출력합니다.

<a name="database-constructor-signature-changes"></a>
#### 데이터베이스 관련 생성자 시그니처 변경 (Database Constructor Signature Changes)

**영향 가능성: 매우 낮음**

Laravel 12부터 몇몇 저수준 데이터베이스 클래스는 생성자에서 반드시 `Illuminate\Database\Connection` 인스턴스를 전달받아야 합니다.

**이 변경은 데이터베이스 패키지 유지보수자에게만 주로 해당하며, 일반적인 애플리케이션 개발에 영향이 갈 가능성은 극히 낮습니다.**

`Illuminate\Database\Schema\Blueprint`

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Connection` 인스턴스를 필요로 합니다. 이것은 Blueprint 인스턴스를 직접 생성하는 애플리케이션 또는 패키지에만 영향을 줍니다.

`Illuminate\Database\Grammar`

`Illuminate\Database\Grammar` 클래스의 생성자에서도 이제 `Connection` 인스턴스가 필요합니다. 이전 버전에서는 생성 후 `setConnection()` 메서드를 이용해 연결(커넥션)을 지정했습니다. 이 메서드는 Laravel 12에서 제거되었습니다:

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
```

또한 다음 API들이 제거 또는 폐기(deprecated)되었습니다:

<div class="content-list" markdown="1">

- `Blueprint::getPrefix()` 메서드는 폐기되었습니다.
- `Connection::withTablePrefix()` 메서드는 삭제되었습니다.
- `Grammar::getTablePrefix()` 및 `setTablePrefix()` 메서드는 폐기되었습니다.
- `Grammar::setConnection()` 메서드는 삭제되었습니다.

</div>

이제 테이블 프리픽스(table prefix)를 사용할 때는 커넥션에서 직접 가져와야 합니다:

```php
$prefix = $connection->getTablePrefix();
```

커스텀 데이터베이스 드라이버, 스키마 빌더, 문법(Grammar) 구현을 유지보수 중이라면, 생성자에서 반드시 `Connection` 인스턴스를 전달하고 있는지 확인해야 합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7 (Models and UUIDv7)

**영향 가능성: 중간**

`HasUuids` 트레잇은 이제 UUID 스펙 버전 7에 호환되는(정렬 가능한) UUID를 반환합니다. (기존에는 v4 사용) 모델의 ID에 계속해서 UUIDv4(순서 있는 v4 UUID 문자열)를 사용하고 싶다면, 이제 `HasVersion4Uuids` 트레잇을 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레잇은 제거되었습니다. 기존에 이 트레잇을 사용했다면, 동일 동작을 하는 `HasUuids` 트레잇으로 교체해야 합니다.

<a name="requests"></a>
### 요청 (Requests)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합 (Nested Array Request Merging)

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용하여 중첩 배열 데이터를 병합할 수 있습니다. 이전에는 이 메서드를 통해 "dot" 표기 키를 최상위 배열의 키로 추가했다면, 새로운 동작에 맞게 코드를 조정해야 합니다:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="routing"></a>
### 라우팅 (Routing)

<a name="route-precedence"></a>
#### 라우트 우선순위 (Route Precedence)

**영향 가능성: 낮음**

여러 라우트에 동일한 이름이 지정된 경우, **캐시된 라우팅과 캐시되지 않은 라우팅의 동작이 통일**되었습니다. 이제 캐시되지 않은 라우팅 역시 동일 라우트명이 여러 개 있을 때 첫 번째로 등록된 라우트를 매칭합니다.

<a name="storage"></a>
### 스토리지 (Storage)

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일시스템 디스크 기본 루트 경로 (Local Filesystem Disk Default Root Path)

**영향 가능성: 낮음**

파일시스템 설정에서 `local` 디스크를 명시적으로 정의하지 않은 경우, Laravel은 이제 local 디스크의 루트를 `storage/app/private`로 기본 설정합니다. 기존에는 `storage/app`이 기본이었습니다. 따라서, `Storage::disk('local')`로 읽고 쓸 때 기본적으로 `storage/app/private` 경로가 사용됩니다. 예전 동작으로 되돌리고 싶으면, `local` 디스크를 직접 정의하고 원하는 루트 경로를 설정하면 됩니다.

<a name="validation"></a>
### 유효성 검증 (Validation)

<a name="image-validation"></a>
#### SVG가 제외된 이미지 유효성 검증 (Image Validation Now Excludes SVGs)

**영향 가능성: 낮음**

`image` 유효성 검증 규칙이 이제 기본적으로 SVG 이미지를 허용하지 않습니다. 만약 `image` 규칙에서 SVG도 허용하고 싶다면, 명시적으로 허용 옵션을 추가해야 합니다:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타 참고 (Miscellaneous)

`laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 이력도 참고하시기 바랍니다. 이들 변경 사항은 꼭 따라야 하는 것은 아니지만, 애플리케이션 소스와 맞춰두면 좋을 수 있습니다. 일부 내용은 본 업그레이드 가이드에서 다루지만, 설정 파일이나 주석 등의 변화는 직접 포함되지 않을 수 있습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용해 변경 내역을 쉽게 확인하고, 필요한 업데이트만 선택적으로 반영할 수 있습니다.
