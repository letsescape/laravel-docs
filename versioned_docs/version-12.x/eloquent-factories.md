# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 이용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스(Sequence)](#sequences)
- [팩토리의 연관관계 설정](#factory-relationships)
    - [Has Many(1:N) 연관관계](#has-many-relationships)
    - [Belongs To(N:1) 연관관계](#belongs-to-relationships)
    - [Many to Many(N:M) 연관관계](#many-to-many-relationships)
    - [폴리모픽 연관관계](#polymorphic-relationships)
    - [팩토리 내에서 연관관계 정의하기](#defining-relationships-within-factories)
    - [기존 모델을 재활용한 연관관계 처리](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스에 시드 데이터를 삽입할 때, 일부 레코드를 데이터베이스에 추가해야 할 수 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/12.x/eloquent)에 대해 모델 팩토리를 이용하여 기본 속성 집합을 정의할 수 있도록 지원합니다.

팩토리 작성 예시는 애플리케이션의 `database/factories/UserFactory.php` 파일에서 확인하실 수 있습니다. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본적으로 포함되어 있으며, 다음과 같은 팩토리 정의를 제공합니다:

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

보시다시피, 가장 기본적인 형태의 팩토리는 Laravel의 기본 팩토리 클래스를 상속하며, `definition` 메서드를 정의합니다. `definition` 메서드는 해당 팩토리로 모델을 생성할 때 적용될 속성 값 집합을 반환합니다.

`fake` 헬퍼를 통해 팩토리에서는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있으며, 이를 통해 테스트와 시딩을 위한 다양한 무작위 데이터를 쉽게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 로케일은 `config/app.php` 설정 파일의 `faker_locale` 옵션을 변경하여 바꿀 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/12.x/artisan)를 실행하십시오.

```shell
php artisan make:factory PostFactory
```

생성된 새 팩토리 클래스는 `database/factories` 디렉토리에 위치합니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 자동 매칭 규칙

팩토리를 정의한 후에는, 모델이 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트를 사용할 때 제공되는 정적 `factory` 메서드를 통해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 모델에 할당된 팩토리에 적합한 클래스를 찾기 위해 약속된 네이밍 룰을 사용합니다. 즉, `Database\Factories` 네임스페이스 내에서, 모델 이름과 동일하며 `Factory`로 끝나는 클래스명을 찾습니다. 만약 이 규칙이 해당 애플리케이션의 상황에 맞지 않는다면, 모델에 `UseFactory` 속성을 추가하여 팩토리를 직접 지정할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

또는, 모델에서 `newFactory` 메서드를 오버라이드하여 직접 팩토리 인스턴스를 반환할 수도 있습니다:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

그리고, 해당 팩토리 클래스에 `model` 속성을 정의해야 합니다:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태(State) (Factory States)

상태(State) 변경 메서드를 활용하면, 팩토리에서 임의의 조합으로 적용할 수 있는 별도의 속성 변형을 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory`에서 기본 속성 중 하나를 수정하는 `suspended` 상태 메서드를 추가할 수 있습니다.

상태 변환 메서드는 보통 Laravel의 기본 팩토리 클래스에서 제공하는 `state` 메서드를 호출합니다. 이 메서드는 팩토리의 원시 속성 배열을 인자로 받아, 수정할 속성 배열을 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a name="trashed-state"></a>
#### "Trashed" 상태

Eloquent 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 소프트 삭제 처리되었음을 바로 지정할 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 사용할 수 있기 때문에 별도의 정의가 필요하지 않습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록하며, 모델 생성(메모리상 또는 DB 저장) 후 추가 동작을 수행할 수 있게 해줍니다. 팩토리 클래스에 `configure` 메서드를 정의하여 이 콜백을 등록할 수 있으며, 팩토리 인스턴스가 생성될 때 Laravel이 자동으로 호출합니다:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // ...
        })->afterCreating(function (User $user) {
            // ...
        });
    }

    // ...
}
```

특정 상태에 한정한 추가 작업이 필요하다면, 상태 메서드 내에서 팩토리 콜백을 등록할 수도 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // ...
    })->afterCreating(function (User $user) {
        // ...
    });
}
```

<a name="creating-models-using-factories"></a>
## 팩토리를 이용한 모델 생성 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스화 (Instantiating Models)

팩토리를 정의한 후에는, 모델에 포함된 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트의 정적 `factory` 메서드를 이용해 해당 모델의 팩토리 인스턴스를 만들 수 있습니다. 몇 가지 모델 생성 예시를 살펴보겠습니다. 먼저, `make` 메서드를 사용하여 데이터베이스에 저장하지 않고 모델 인스턴스만 생성할 수 있습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 활용하면 여러 개의 모델 컬렉션을 생성할 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태(State) 적용하기

정의한 [상태](#factory-states)를 원하는 모델에 적용할 수도 있습니다. 여러 상태 변환을 적용하고 싶다면, 상태 변환 메서드를 연속해서 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 값 오버라이드

기본 속성 값 중 일부만 덮어쓰고 싶다면, `make` 메서드에 배열로 원하는 속성 값을 전달하면 됩니다. 지정된 속성만 새 값으로 대체되고, 나머지는 팩토리에서 정의된 기본값이 그대로 적용됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, `state` 메서드를 직접 팩토리 인스턴스에 호출하여 인라인 상태 변환을 할 수도 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용해 모델을 생성할 때는 [대량 할당 보호](/docs/12.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성한 후 Eloquent의 `save` 메서드를 통해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// App\Models\User 인스턴스 한 개 생성...
$user = User::factory()->create();

// App\Models\User 인스턴스 세 개 생성...
$users = User::factory()->count(3)->create();
```

`create` 메서드에 속성 배열을 전달하면, 팩토리의 기본 속성 값을 개별적으로 오버라이드할 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequence)

여러 모델을 생성하면서 특정 속성 값을 번갈아가며 지정하고 싶을 때가 있습니다. 이럴 때는 상태 변환을 시퀀스로 지정할 수 있습니다. 예를 들어, 생성되는 각 유저의 `admin` 컬럼 값을 차례로 `Y`, `N`으로 반복해서 할당하려면 다음과 같이 하면 됩니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        ['admin' => 'Y'],
        ['admin' => 'N'],
    ))
    ->create();
```

위 예시에서는 5명의 유저가 `admin` 값이 `Y`, 5명이 `N`으로 생성됩니다.

필요하다면 시퀀스 값에 클로저를 전달할 수도 있습니다. 이 클로저는 시퀀스가 새로운 값을 필요로 할 때마다 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

클로저 내부에서 시퀀스 인스턴스의 `$index` 속성에 접근할 수 있습니다. 이 값은 시퀀스의 반복 횟수를 나타냅니다:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

편의상, 내부적으로 `state`를 호출하는 `sequence` 메서드로도 시퀀스를 적용할 수 있습니다. 이 메서드는 클로저 또는 속성 배열을 전달받습니다:

```php
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```

<a name="factory-relationships"></a>
## 팩토리의 연관관계 설정 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many(1:N) 연관관계

이번에는 Laravel의 유연한 팩토리 메서드를 이용해 Eloquent 모델 간 연관관계를 생성하는 방법을 살펴봅니다. 예를 들어, 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User` 모델은 `Post`와 hasMany 연관관계를 가진다고 가정합시다. 이때, 팩토리의 `has` 메서드에 팩토리 인스턴스를 전달하여 세 개의 게시글을 가진 유저를 생성할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

`has` 메서드에 `Post` 모델을 전달할 경우, Laravel은 `User` 모델에 `posts`라는 연관관계 메서드가 존재함을 가정합니다. 필요하다면 조작하려는 연관관계의 이름을 명시적으로 전달할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관된 모델에 상태 변환도 적용할 수 있습니다. 또한, 부모 모델에 접근해야 할 때는 클로저 기반의 상태 변환도 넘길 수 있습니다:

```php
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
    )
    ->create();
```

<a name="has-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

더 편리하게 라라벨의 "매직 팩토리 연관관계 메서드"도 지원합니다. 아래 예시에서, Laravel은 규칙에 따라 `User` 모델의 `posts` 연관관계 메서드를 이용해 관련 모델을 생성합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때, 연관 모델의 속성을 덮어쓸 배열도 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변환이 부모 모델에 접근해야 할 경우에는, 클로저를 두 번째 인수로 전달할 수도 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To(N:1) 연관관계

이제 "has many"와 반대되는 연관관계인 "belongs to" 관계의 팩토리 사용법을 살펴봅니다. 팩토리에서 생성한 모델이 소속될 부모 모델을 `for` 메서드로 정의할 수 있습니다. 예를 들어, 하나의 유저(부모)에 소속된 `App\Models\Post` 모델 인스턴스 세 개를 만들려면 다음과 같이 합니다:

```php
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```

이미 존재하는 부모 모델 인스턴스가 있다면, `for` 메서드에 해당 인스턴스를 바로 넘길 수도 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

"belongs to" 관계 역시 매직 팩토리 연관관계 메서드로 정의할 수 있습니다. 아래 예제는 세 개의 게시글이 `Post` 모델의 `user` 연관관계에 소속됨을 의미합니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many(N:M) 연관관계

[Has many 연관관계](#has-many-relationships)와 마찬가지로, "many to many" 관계 역시 `has` 메서드를 사용해 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot 테이블 속성

모델을 연결하는 중간 테이블(피벗 테이블)에 속성을 추가로 지정해야 한다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수에 피벗 테이블의 속성명과 값을 배열로 전달합니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```

상태 변경이 연관 모델에 접근해야 한다면, 클로저 기반의 상태 변환을 전달할 수도 있습니다:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['name' => $user->name.' Role'];
            }),
        ['active' => true]
    )
    ->create();
```

이미 존재하는 모델 인스턴스를 새로 생성하는 모델에 연결하고 싶을 때도 `hasAttached` 메서드에 해당 인스턴스(또는 컬렉션)를 전달하면 됩니다. 이 예시에서는 동일한 세 개의 역할이 모든 유저에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

깔끔하게, many to many 관계 역시 매직 팩토리 연관관계 메서드로 정의할 수 있습니다. 아래 예시는 `User` 모델의 `roles` 연관관계를 이용해 관련 모델을 생성합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽 연관관계 (Polymorphic Relationships)

[폴리모픽 연관관계](/docs/12.x/eloquent-relationships#polymorphic-relationships) 역시 팩토리를 사용해 생성할 수 있습니다. 폴리모픽 morphMany 관계는 일반적인 hasMany 관계와 동일하게 팩토리를 활용하면 됩니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment`와 morphMany 관계를 가질 때:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 연관관계

`morphTo` 연관관계를 만들 때는 매직 메서드를 사용할 수 없습니다. 대신, `for` 메서드를 직접 사용하고, 관계의 이름도 명시적으로 전달해야 합니다. 예를 들어, `Comment` 모델이 `commentable`이라는 morphTo 관계를 가진다면, 다음과 같이 작성합니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 Many to Many 관계

폴리모픽 "many to many"(`morphToMany` / `morphedByMany`) 관계는 일반적인 many to many와 동일한 방식으로 생성할 수 있습니다:

```php
use App\Models\Tag;
use App\Models\Video;

$video = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

매직 `has` 메서드로도 폴리모픽 many to many 관계 생성을 지원합니다:

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 연관관계 정의하기

모델 팩토리 내에서 연관관계를 정의하려면, 보통 외래키 속성에 새 팩토리 인스턴스를 지정합니다. 이는 주로 `belongsTo`, `morphTo` 등 "역방향" 관계에서 필요합니다. 예를 들어, 게시글(Post)을 생성할 때 자동으로 새로운 유저가 생성되도록 하려면:

```php
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

연관관계의 컬럼이 팩토리에서 정의된 다른 속성에 의존한다면, 속성에 클로저를 지정하여 팩토리 평가 결과를 참조할 수도 있습니다:

```php
/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a name="recycling-an-existing-model-for-relationships"></a>
### 기존 모델을 재활용한 연관관계 처리

여러 모델이 동일한 연관관계(예: 공통 부모 모델)를 가질 때, 팩토리에서 생성되는 모든 연관관계에 동일한 관련 모델 인스턴스가 쓰이도록 하려면 `recycle` 메서드를 사용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델 구조가 있고, 티켓과 항공편 모두 항공사와 연관되며, 티켓 생성 시 티켓과 항공편에 동일한 항공사가 연결되길 원한다면, `recycle` 메서드에 항공사 인스턴스를 전달하면 됩니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 공통된 유저, 팀 등 여러 모델에 유용하게 활용할 수 있습니다.

또한, `recycle` 메서드는 기존 모델 컬렉션도 받을 수 있습니다. 컬렉션을 전달하면, 팩토리가 해당 타입의 모델을 필요로 할 때 무작위로 하나씩 선택해 사용하게 됩니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```