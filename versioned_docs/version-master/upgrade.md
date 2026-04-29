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
- [이미지 유효성 검증에서 이제 SVG 제외](#image-validation)
- [로컬 파일시스템 디스크 기본 루트 경로](#local-filesystem-disk-default-root-path)
- [다중 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드 (Upgrading To 12.0 From 11.x)

#### 예상 업그레이드 시간: 5분

> [!NOTE]
> 가능한 모든 호환성 깨짐 변경 사항을 문서화하려고 노력합니다. 이 변경 사항 중 일부는 프레임워크의 잘 쓰이지 않는 부분에 있으므로, 실제로는 이 중 일부만 애플리케이션에 영향을 줄 수 있습니다. 시간을 아끼고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하면 애플리케이션 업그레이드를 자동화하는 데 도움을 받을 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`를 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

Carbon 2.x 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)가 필요합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel Installer 업데이트

Laravel installer CLI 도구를 사용하여 새 Laravel 애플리케이션을 만들고 있다면, Laravel 12.x 및 [새 Laravel 스타터 키트](https://laravel.com/starter-kits)와 호환되도록 installer 설치를 업데이트해야 합니다. `composer global require`로 Laravel installer를 설치했다면, `composer global update`를 사용하여 installer를 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

원래 `php.new`를 통해 PHP와 Laravel을 설치했다면, 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 Laravel installer를 설치할 수 있습니다.

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

또는 [Laravel Herd](https://herd.laravel.com)에 포함된 Laravel installer 사본을 사용하고 있다면, Herd 설치를 최신 릴리스로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### 업데이트된 `DatabaseTokenRepository` 생성자 시그니처

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자는 이제 `$expires` 파라미터를 분 단위가 아니라 초 단위로 받습니다.

<a name="concurrency"></a>
### Concurrency

<a name="concurrency-result-index-mapping"></a>
#### Concurrency 결과 인덱스 매핑

**영향 가능성: 낮음**

연관 배열로 `Concurrency::run` 메서드를 호출하면, 동시 작업의 결과가 이제 해당 키와 함께 반환됩니다.

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
### 컨테이너

<a name="container-class-dependency-resolution"></a>
#### 컨테이너 클래스 의존성 해결

**영향 가능성: 낮음**

의존성 주입 컨테이너는 이제 클래스 인스턴스를 해결할 때 클래스 속성의 기본값을 존중합니다. 이전에 컨테이너가 기본값 없이 클래스 인스턴스를 해결하는 동작에 의존하고 있었다면, 이 새로운 동작을 고려하도록 애플리케이션을 조정해야 할 수 있습니다.

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
### 데이터베이스

<a name="multi-schema-database-inspecting"></a>
#### 다중 스키마 데이터베이스 검사

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마의 결과만 가져오려면 `schema` 인수를 전달할 수 있습니다.

```php
// All tables on all schemas...
$tables = Schema::getTables();

// All tables on the 'main' schema...
$tables = Schema::getTables(schema: 'main');

// All tables on the 'main' and 'blog' schemas...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 포함된 테이블 이름을 반환합니다. 원하는 동작으로 변경하려면 `schemaQualified` 인수를 전달할 수 있습니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령어는 이제 PostgreSQL 및 SQL Server와 마찬가지로 MySQL, MariaDB, SQLite에서도 모든 스키마의 결과를 출력합니다.

<a name="database-constructor-signature-changes"></a>
#### 데이터베이스 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

Laravel 12에서는 여러 저수준 데이터베이스 클래스가 생성자를 통해 `Illuminate\Database\Connection` 인스턴스를 제공받아야 합니다.

**이 변경 사항은 주로 데이터베이스 패키지 유지보수자에게 적용됩니다. 일반적인 애플리케이션 개발에 영향을 줄 가능성은 극히 낮습니다.**

`Illuminate\Database\Schema\Blueprint`

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Connection` 인스턴스를 기대합니다. 이는 주로 `Blueprint` 인스턴스를 직접 생성하는 애플리케이션이나 패키지에 영향을 줍니다.

`Illuminate\Database\Grammar`

`Illuminate\Database\Grammar` 클래스의 생성자도 이제 `Connection` 인스턴스가 필요합니다. 이전 버전에서는 생성 후 `setConnection()` 메서드를 사용하여 연결을 할당했습니다. 이 메서드는 Laravel 12에서 제거되었습니다.

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
````

또한 다음 API는 제거되었거나 사용 중단 예정입니다.

<div class="content-list" markdown="1">

- `Blueprint::getPrefix()` 메서드는 사용 중단 예정입니다.
- `Connection::withTablePrefix()` 메서드는 제거되었습니다.
- `Grammar::getTablePrefix()` 및 `setTablePrefix()` 메서드는 사용 중단 예정입니다.
- `Grammar::setConnection()` 메서드는 제거되었습니다.

</div>

테이블 접두사를 다룰 때는 이제 데이터베이스 연결에서 직접 가져와야 합니다.

```php
$prefix = $connection->getTablePrefix();
```

커스텀 데이터베이스 드라이버, 스키마 빌더, 또는 grammar 구현을 유지보수하고 있다면, 생성자를 검토하고 `Connection` 인스턴스가 제공되는지 확인해야 합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7

**영향 가능성: 중간**

`HasUuids` trait는 이제 UUID 사양의 버전 7과 호환되는 UUID(정렬된 UUID)를 반환합니다. 모델 ID에 대해 정렬된 UUIDv4 문자열을 계속 사용하려면 이제 `HasVersion4Uuids` trait를 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` trait는 제거되었습니다. 이전에 이 trait를 사용하고 있었다면, 이제 동일한 동작을 제공하는 `HasUuids` trait를 대신 사용해야 합니다.

<a name="requests"></a>
### 요청

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용하여 중첩 배열 데이터를 병합할 수 있습니다. 이전에 이 메서드가 "dot" 표기법 버전의 키를 포함하는 최상위 배열 키를 생성하는 동작에 의존하고 있었다면, 이 새로운 동작을 고려하도록 애플리케이션을 조정해야 할 수 있습니다.

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="routing"></a>
### 라우팅

<a name="route-precedence"></a>
#### 라우트 우선순위

**영향 가능성: 낮음**

동일한 이름을 가진 여러 라우트가 있을 때의 라우팅 동작이 캐시된 라우팅과 캐시되지 않은 라우팅 사이에서 통일되었습니다. 즉, 캐시되지 않은 라우팅은 이제 특정 이름으로 등록된 마지막 라우트가 아니라 첫 번째 라우트와 매칭됩니다.

<a name="storage"></a>
### 스토리지

<a name="local-filesystem-disk-default-root-path"></a>
#### 로컬 파일시스템 디스크 기본 루트 경로

**영향 가능성: 낮음**

애플리케이션의 filesystems 설정에서 `local` 디스크를 명시적으로 정의하지 않은 경우, Laravel은 이제 로컬 디스크의 루트를 기본적으로 `storage/app/private`로 설정합니다. 이전 릴리스에서는 기본값이 `storage/app`이었습니다. 따라서 별도로 설정하지 않으면 `Storage::disk('local')` 호출은 `storage/app/private`에서 읽고 이 위치에 씁니다. 이전 동작으로 되돌리려면 `local` 디스크를 직접 정의하고 원하는 루트 경로를 설정하면 됩니다.

<a name="validation"></a>
### 유효성 검증

<a name="image-validation"></a>
#### 이미지 유효성 검증에서 이제 SVG 제외

**영향 가능성: 낮음**

`image` 유효성 검증 규칙은 더 이상 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙을 사용할 때 SVG를 허용하려면 명시적으로 허용해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// Or...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타

또한 `laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 사항도 확인해 보시기를 권장합니다. 이러한 변경 사항 중 많은 부분은 필수는 아니지만, 애플리케이션의 파일을 최신 상태로 맞춰 두고 싶을 수 있습니다. 이 업그레이드 가이드에서 일부 변경 사항을 다루지만, 설정 파일이나 주석 변경과 같은 다른 변경 사항은 다루지 않습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용하면 변경 사항을 쉽게 확인하고, 어떤 업데이트가 자신에게 중요한지 선택할 수 있습니다.
