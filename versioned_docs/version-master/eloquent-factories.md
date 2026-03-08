# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 이용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리의 연관관계](#factory-relationships)
    - [Has Many 연관관계](#has-many-relationships)
    - [Belongs To 연관관계](#belongs-to-relationships)
    - [Many to Many 연관관계](#many-to-many-relationships)
    - [다형성 연관관계](#polymorphic-relationships)
    - [팩토리 내부에서 연관관계 정의하기](#defining-relationships-within-factories)
    - [연관관계에서 기존 모델 재사용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스에 시딩할 때 데이터베이스에 몇 개의 레코드를 삽입해야 할 때가 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/master/eloquent)마다 기본 속성(attribute) 집합을 팩토리로 정의할 수 있습니다.

팩토리를 작성하는 예제를 확인하려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 살펴보십시오. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 포함되어 있으며 다음과 같은 팩토리 정의를 가지고 있습니다:

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

보시다시피, 가장 기본적인 형태에서 팩토리는 Laravel의 기본 팩토리 클래스를 상속받아, `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 이용해 모델을 생성할 때 적용되는 기본 속성 값 배열을 반환합니다.

팩토리에서는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있어, 테스트 및 시딩에 사용할 다양한 랜덤 데이터를 쉽게 만들 수 있습니다.

> [!NOTE]
> 애플리케이션에서 Faker의 언어(locale)를 변경하려면 `config/app.php` 설정 파일의 `faker_locale` 옵션을 수정하면 됩니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면, `make:factory` [Artisan 명령어](/docs/master/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새로 생성된 팩토리 클래스는 애플리케이션의 `database/factories` 디렉토리에 저장됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 자동 탐색 규칙

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 모델에 할당된 팩토리에 대해, 네이밍 규칙을 활용해 올바른 팩토리를 자동으로 찾습니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스에 위치하고, 모델 이름과 동일하며 `Factory`로 끝나는 이름의 클래스를 찾습니다. 만약 이런 규칙이 해당 애플리케이션이나 팩토리에 적용되지 않는다면, 모델에 `UseFactory` 속성(attribute)을 추가해 수동으로 팩토리를 지정할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

또는, 모델에서 `newFactory` 메서드를 오버라이드 해 직접 팩토리 인스턴스를 반환할 수도 있습니다:

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

그리고, 해당 팩토리에서는 `UseModel` 속성을 사용해 어떤 모델을 위한 팩토리인지 명시할 수 있습니다:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Attributes\UseModel;
use Illuminate\Database\Eloquent\Factories\Factory;

#[UseModel(Flight::class)]
class FlightFactory extends Factory
{
    // ...
}
```

<a name="factory-states"></a>
### 팩토리 상태(State) (Factory States)

상태 변환(state manipulation) 메서드를 통해, 팩토리에 다양한 조합으로 적용할 수 있는 개별 변형을 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에 기본 속성 값을 변경하는 `suspended` 상태 메서드를 추가할 수 있습니다.

상태 변환 메서드는 일반적으로 Laravel 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리의 원시 속성 배열을 받아 수정할 속성 배열을 반환하는 클로저를 인수로 받습니다:

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
#### "삭제됨(Trashed)" 상태

Eloquent 모델이 [소프트 삭제](/docs/master/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 사용하여 생성된 모델이 이미 "소프트 삭제"된 상태로 만들 수 있습니다. 이 `trashed` 상태는 자동으로 모든 팩토리에 제공되므로, 직접 정의할 필요가 없습니다.

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking`과 `afterCreating` 메서드로 등록하며, 모델 생성 후 추가 작업을 수행할 수 있게 합니다. 이 콜백은 팩토리 클래스의 `configure` 메서드를 정의함으로써 등록하며, 팩토리 인스턴스화 시 Laravel이 자동으로 호출합니다:

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

또한, 상태 메서드 내부에서도 특정 상태에 맞는 추가 작업을 위한 콜백을 등록할 수 있습니다:

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

팩토리를 정의한 후에는, 모델이 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트를 포함하고 있다면 정적 `factory` 메서드를 사용하여 팩토리 인스턴스를 생성할 수 있습니다. 먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않고 모델을 생성하는 예시를 살펴보겠습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 통해 여러 개의 모델 컬렉션도 생성할 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

[상태 변환](#factory-states)을 모델에 적용할 수도 있습니다. 여러 상태 변환 메서드를 직접 체이닝하여 동시에 적용할 수 있습니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 오버라이드하기

팩토리에서 정의한 기본값 대신, 일부 속성만 직접 지정하려면 `make` 메서드에 값을 배열로 전달할 수 있습니다. 지정한 속성만 대체되고, 나머지는 팩토리 기본값이 사용됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, 팩토리 인스턴스에 `state` 메서드를 직접 호출해 인라인으로 상태 변환을 적용할 수도 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리로 모델을 생성할 때 [대량 할당 보호(mass assignment protection)](/docs/master/eloquent#mass-assignment)는 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 이용해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// App\Models\User 인스턴스 한 개 생성
$user = User::factory()->create();

// App\Models\User 인스턴스 세 개 생성
$users = User::factory()->count(3)->create();
```

그리고, `create` 메서드에도 속성을 배열로 전달해 기본값을 오버라이드할 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequences)

여러 모델을 생성할 때, 특정 속성의 값을 번갈아가며 할당하고 싶을 때는 상태 변환을 시퀀스(Sequence)로 정의할 수 있습니다. 예를 들어, 각 사용자 생성 시 `admin` 칼럼의 값을 `Y`와 `N`으로 번갈아주고 싶다면:

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

이 예시에서는 10명의 사용자 중 5명은 `admin`이 `Y`이고, 나머지 5명은 `N`입니다.

필요하다면, 시퀀스 값으로 클로저를 제공할 수도 있습니다. 이 경우, 새 시퀀스 값이 필요할 때마다 클로저가 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에서는 시퀀스 인스턴스의 `$index` 프로퍼티에 접근할 수 있는데, 이 값은 지금까지 시퀀스가 반복된 횟수를 나타냅니다:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

시퀀스를 더 간편하게 적용하고 싶다면, 내부적으로 `state`를 호출하는 `sequence` 메서드를 사용할 수도 있습니다. `sequence` 메서드는 클로저 또는 배열로 시퀀스 속성 값을 받습니다:

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
## 팩토리의 연관관계 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 연관관계

이제 Laravel의 유연한(factory) 메서드를 사용해 Eloquent 모델 간의 연관관계를 구성해보겠습니다. 먼저, 애플리케이션에 `App\Models\User`와 `App\Models\Post` 모델이 있다고 가정하고, `User` 모델이 `Post`와 hasMany 연관관계를 정의한다고 합시다. `has` 메서드를 이용하여, 1명의 사용자가 3개의 게시글을 갖도록 만들 수 있습니다. `has` 메서드에는 팩토리 인스턴스를 전달합니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `Post` 모델을 `has` 메서드에 전달하면 Laravel은 `User` 모델에 `posts` 메서드가 존재해 연관관계를 정의한다고 가정합니다. 필요하다면, 조작하려는 연관관계의 이름을 명시적으로 지정할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관된 모델에도 상태 변환을 적용할 수 있습니다. 또한, 상태 변환시 부모 모델에 접근이 필요한 경우 클로저 기반의 상태 변환을 전달할 수도 있습니다:

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
#### 매직 메서드(Magic Methods) 활용

더 편리하게 연관관계를 정의하려면, Laravel의 매직 팩토리 연관관계 메서드를 사용할 수 있습니다. 아래 예시처럼, `hasPosts`와 같은 메서드를 이용하면 Laravel은 자동으로 `User` 모델의 `posts` 메서드를 통해 관련 모델을 생성합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때, 연관된 모델의 속성을 배열로 재정의할 수도 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변환 시 부모 모델에 접근이 필요한 경우, 클로저 기반 상태 변환을 넘길 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 연관관계

앞서 "has many" 연관관계를 팩토리로 생성하는 방법을 살펴봤다면, 이제 그 반대 연관관계도 살펴보겠습니다. 팩토리에서 모델이 속할 부모 모델을 정의하려면 `for` 메서드를 사용하면 됩니다. 예를 들어, 하나의 유저에 속한 3개의 `App\Models\Post` 모델 인스턴스를 생성하려면 다음과 같이 작성합니다:

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

이미 생성된 부모 모델 인스턴스가 있다면, 해당 인스턴스를 `for` 메서드에 직접 전달할 수 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드(Using Magic Methods)

매직 팩토리 연관관계 메서드를 이용해 "belongs to" 연관관계도 정의할 수 있습니다. 아래 예시는, 세 개의 게시글이 `Post` 모델의 `user` 연관관계에 속하게 생성합니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many 연관관계

[has many 연관관계](#has-many-relationships)와 마찬가지로, 다대다(Many to Many) 연관관계도 `has` 메서드로 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot(중간) 테이블 속성 지정

연관 모델을 연결하는 pivot(중간) 테이블에 값을 지정하고 싶다면, `hasAttached` 메서드를 사용하면 됩니다. 이 메서드의 두 번째 인수로 중간 테이블의 필드와 값을 배열로 넘길 수 있습니다:

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

연관모델에 접근해 상태 변환이 필요하다면, 클로저 기반의 상태 변환도 전달할 수 있습니다:

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

이미 생성된 모델 인스턴스를 연관관계로 연결하고 싶다면, 해당 인스턴스들을 `hasAttached` 메서드로 전달하면 됩니다. 아래 예시에서는 같은 세 개의 Role이 세 명의 사용자 모두에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 활용

매직 팩토리 연관관계 메서드를 활용해 다대다 관계도 정의할 수 있습니다. 아래 예제는 `User` 모델의 `roles` 메서드를 통해 연관 모델을 생성합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 연관관계 (Polymorphic Relationships)

[다형성 연관관계](/docs/master/eloquent-relationships#polymorphic-relationships)도 팩토리로 생성할 수 있습니다. 다형성 "morph many" 연관관계는 일반 "has many"와 동일한 방식으로 생성합니다. 예를 들어, `App\Models\Post`가 `App\Models\Comment`와 morphMany 관계를 가진다면:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 연관관계

매직 메서드는 `morphTo` 연관관계 생성에는 사용할 수 없습니다. 대신, `for` 메서드를 직접 사용하고, 연관관계 이름도 명시해야 합니다. 아래는 `Comment` 모델의 `commentable` 메서드가 `morphTo` 관계를 정의하는 경우, 세 개의 댓글이 한 포스트에 속하도록 만드는 예시입니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 다대다(Polymorphic Many to Many) 연관관계

다형성 "다대다(morphToMany / morphedByMany)" 연관관계 역시 일반 "다대다"와 동일하게 팩토리로 만들 수 있습니다:

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

물론, 매직 `has` 메서드로도 다형성 "다대다" 연관관계를 만들 수 있습니다:

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내부에서 연관관계 정의하기

모델 팩토리 내부에서 연관관계를 정의하려면, 주로 관계의 "역방향"(`belongsTo`, `morphTo`)일 때 외래 키에 새로운 팩토리 인스턴스를 할당합니다. 예를 들어, 포스트를 만들 때마다 새로운 유저를 생성하고 싶다면 아래처럼 작성할 수 있습니다:

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

연관관계 컬럼이 팩토리를 정의하는 다른 속성값에 따라 달라진다면, 해당 속성에 클로저를 할당해 처리할 수 있습니다. 이 클로저에는 평가(evaluated)된 팩토리 속성 배열이 전달됩니다:

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
### 연관관계에서 기존 모델 재사용하기

여러 모델이 하나의 공통 연관관계를 가질 때, `recycle` 메서드를 사용하여 팩토리에서 생성되는 모든 연관관계에 대해 동일한 연관 모델 인스턴스를 재사용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있다고 가정해봅니다. 하나의 티켓은 항공사와 항공편에 각각 속하고, 해당 항공편 역시 항공사에 속합니다. 티켓을 생성할 때 티켓과 항공편 모두 동일한 항공사를 갖도록 하고 싶다면, 항공사 인스턴스를 `recycle` 메서드에 전달하면 됩니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

이와 같이 `recycle` 메서드는 공통 User나 Team에 속하는 모델이 있을 때도 매우 유용합니다.

`recycle` 메서드에는 기존 모델의 컬렉션도 전달할 수 있습니다. 이 경우, 팩토리가 해당 타입의 모델이 필요할 때마다 컬렉션에서 무작위 인스턴스가 선택됩니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
