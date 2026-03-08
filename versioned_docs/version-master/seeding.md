# 데이터베이스: 시딩 (Database: Seeding)

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
    - [모델 이벤트 비활성화하기](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 시더 클래스를 사용하여 데이터베이스에 데이터를 채우는 기능을 포함합니다. 모든 시더 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 정의되어 있으며, 이 클래스에서 `call` 메서드를 사용해 다른 시더 클래스를 실행할 수 있어 시딩 실행 순서를 제어할 수 있습니다.

> [!NOTE]
> 데이터베이스 시딩 중에는 [대량 할당 보호](/docs/master/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기 (Writing Seeders)

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/master/artisan)를 실행하세요. 프레임워크로 생성된 모든 시더는 `database/seeders` 디렉터리에 위치합니다:

```shell
php artisan make:seeder UserSeeder
```

시더 클래스는 기본적으로 `run` 메서드만 포함합니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/master/artisan) 실행 시 호출됩니다. `run` 메서드 내에서는 자유롭게 데이터베이스에 데이터를 삽입할 수 있습니다. 직접 [쿼리 빌더](/docs/master/queries)를 사용해 데이터를 삽입하거나, [Eloquent 모델 팩토리](/docs/master/eloquent-factories)를 사용할 수 있습니다.

예를 들어, 기본 `DatabaseSeeder` 클래스를 수정하여 `run` 메서드에 데이터베이스 삽입 문을 추가해 보겠습니다:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        DB::table('users')->insert([
            'name' => Str::random(10),
            'email' => Str::random(10).'@example.com',
            'password' => Hash::make('password'),
        ]);
    }
}
```

> [!NOTE]
> `run` 메서드 시그니처에 필요한 의존성을 타입 힌트로 지정하면, Laravel [서비스 컨테이너](/docs/master/container)를 통해 자동으로 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

물론, 각 모델 시드에 대해 속성을 수동으로 지정하는 것은 번거롭습니다. 대신 [모델 팩토리](/docs/master/eloquent-factories)를 사용하여 많은 양의 데이터 레코드를 편리하게 생성할 수 있습니다. 먼저 [모델 팩토리 문서](/docs/master/eloquent-factories)를 참고하여 팩토리 정의 방법을 익히세요.

예를 들어, 각각 하나의 연관된 게시물을 가진 사용자 50명을 생성해보겠습니다:

```php
use App\Models\User;

/**
 * Run the database seeders.
 */
public function run(): void
{
    User::factory()
        ->count(50)
        ->hasPosts(1)
        ->create();
}
```

<a name="calling-additional-seeders"></a>
### 추가 시더 호출하기

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 사용해 다른 시더 클래스를 실행할 수 있습니다. `call` 메서드를 사용하면 데이터베이스 시딩 과정을 여러 파일로 나누어 한 시더 클래스가 너무 커지지 않도록 관리할 수 있습니다. `call` 메서드는 실행할 시더 클래스 배열을 인수로 받습니다:

```php
/**
 * Run the database seeders.
 */
public function run(): void
{
    $this->call([
        UserSeeder::class,
        PostSeeder::class,
        CommentSeeder::class,
    ]);
}
```

<a name="muting-model-events"></a>
### 모델 이벤트 비활성화하기

시딩 실행 중에 모델 이벤트가 발생하는 것을 막고 싶다면 `WithoutModelEvents` 트레이트를 사용할 수 있습니다. 이 트레이트를 사용하면 `call` 메서드를 통해 추가 시더를 실행해도 어떤 모델 이벤트도 발생하지 않습니다:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
        ]);
    }
}
```

<a name="running-seeders"></a>
## 시더 실행하기 (Running Seeders)

`db:seed` Artisan 명령어를 실행하여 데이터베이스에 시딩할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스는 다른 시더 클래스를 호출할 수 있습니다. 특정 시더 클래스만 실행하려면 `--class` 옵션을 사용합니다:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

또한 `migrate:fresh` 명령어와 `--seed` 옵션을 조합하여 모든 테이블을 삭제하고 모든 마이그레이션을 재실행한 후 시딩을 수행할 수 있습니다. 이 명령어는 데이터베이스를 완전히 재구축할 때 유용합니다. `--seeder` 옵션으로 특정 시더를 지정할 수 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder
```

<a name="forcing-seeding-production"></a>
#### 운영 환경에서 시딩 강제 실행하기

일부 시딩 작업은 데이터를 변경하거나 손실시킬 수 있으므로, `production` 환경에서 시딩 명령 실행 시 확인 메시지가 표시되어 실수를 방지합니다. 확인 절차 없이 시더를 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force
```