<!-- # Eloquent: Factories -->
# Eloquent: Factories

- [Introduction](#introduction)
- [Defining Model Factories](#defining-model-factories)
    - [Generating Factories](#generating-factories)
    - [Factory States](#factory-states)
    - [Factory Callbacks](#factory-callbacks)
- [Creating Models Using Factories](#creating-models-using-factories)
    - [Instantiating Models](#instantiating-models)
    - [Persisting Models](#persisting-models)
    - [Sequences](#sequences)
- [Factory Relationships](#factory-relationships)
    - [Has Many Relationships](#has-many-relationships)
    - [Belongs To Relationships](#belongs-to-relationships)
    - [Many to Many Relationships](#many-to-many-relationships)
    - [Polymorphic Relationships](#polymorphic-relationships)
    - [Defining Relationships Within Factories](#defining-relationships-within-factories)
    - [Recycling an Existing Model for Relationships](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When testing your application or seeding your database, you may need to insert a few records into your database. Instead of manually specifying the value of each column, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/master/eloquent) using model factories. -->
애플리케이션을 테스트하거나 데이터베이스에 시딩할 때, 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 각 컬럼의 값을 직접 지정하는 대신, Laravel은 모델 팩토리를 사용하여 각각의 [Eloquent models](/docs/master/eloquent)에 대한 기본 속성 집합을 정의할 수 있게 해줍니다.

<!-- To see an example of how to write a factory, take a look at the `database/factories/UserFactory.php` file in your application. This factory is included with all new Laravel applications and contains the following factory definition: -->
팩토리를 작성하는 예시를 보려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 살펴보세요. 이 팩토리는 모든 새 Laravel 애플리케이션에 포함되어 있으며, 다음과 같은 팩토리 정의를 담고 있습니다.

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

<!-- As you can see, in their most basic form, factories are classes that extend Laravel's base factory class and define a `definition` method. The `definition` method returns the default set of attribute values that should be applied when creating a model using the factory. -->
보시다시피, 가장 기본적인 형태의 팩토리는 Laravel의 기본 팩토리 클래스를 확장하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 사용해 모델을 생성할 때 적용할 기본 속성 값 집합을 반환합니다.

<!-- Via the `fake` helper, factories have access to the [Faker](https://github.com/FakerPHP/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing and seeding. -->
`fake` 헬퍼를 통해 팩토리는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있습니다. 이 라이브러리를 사용하면 테스트와 시딩에 필요한 여러 종류의 무작위 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]
> `config/app.php` 설정 파일의 `faker_locale` 옵션을 업데이트하여 애플리케이션의 Faker 로케일을 변경할 수 있습니다.

<a name="defining-model-factories"></a>
<!-- ## Defining Model Factories -->
## Defining Model Factories

<a name="generating-factories"></a>
<!-- ### Generating Factories -->
### Generating Factories

<!-- To create a factory, execute the `make:factory` [Artisan command](/docs/master/artisan): -->
팩토리를 생성하려면 `make:factory` [Artisan command](/docs/master/artisan)를 실행하세요.

```shell
php artisan make:factory PostFactory
```

<!-- The new factory class will be placed in your `database/factories` directory. -->
새 팩토리 클래스는 `database/factories` 디렉터리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
<!-- #### Model and Factory Discovery Conventions -->
#### Model and Factory Discovery Conventions

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. -->
팩토리를 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` trait이 모델에 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

<!-- The `HasFactory` trait's `factory` method will use conventions to determine the proper factory for the model the trait is assigned to. Specifically, the method will look for a factory in the `Database\Factories` namespace that has a class name matching the model name and is suffixed with `Factory`. If these conventions do not apply to your particular application or factory, you may add the `UseFactory` attribute to the model to manually specify the model's factory: -->
`HasFactory` trait의 `factory` 메서드는 규칙을 사용하여 trait이 적용된 모델에 알맞은 팩토리를 결정합니다. 구체적으로 이 메서드는 `Database\Factories` 네임스페이스에서 모델명과 일치하고 끝에 `Factory`가 붙은 클래스명을 가진 팩토리를 찾습니다. 이러한 규칙이 특정 애플리케이션이나 팩토리에 맞지 않는 경우, 모델에 `UseFactory` 속성을 추가하여 모델의 팩토리를 직접 지정할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

<!-- Alternatively, you may overwrite the `newFactory` method on your model to return an instance of the model's corresponding factory directly: -->
또는 모델의 `newFactory` 메서드를 재정의하여 해당 모델에 대응하는 팩토리 인스턴스를 직접 반환할 수도 있습니다.

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

<!-- Then, use the `UseModel` attribute on the corresponding factory to specify the model: -->
그런 다음 대응하는 팩토리에서 `UseModel` 속성을 사용하여 모델을 지정합니다.

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
<!-- ### Factory States -->
### Factory States

<!-- State manipulation methods allow you to define discrete modifications that can be applied to your model factories in any combination. For example, your `Database\Factories\UserFactory` factory might contain a `suspended` state method that modifies one of its default attribute values. -->
상태 조작 메서드를 사용하면 모델 팩토리에 어떤 조합으로든 적용할 수 있는 개별 수정 사항을 정의할 수 있습니다. 예를 들어 `Database\Factories\UserFactory` 팩토리는 기본 속성 값 중 하나를 변경하는 `suspended` 상태 메서드를 가질 수 있습니다.

<!-- State transformation methods typically call the `state` method provided by Laravel's base factory class. The `state` method accepts a closure which will receive the array of raw attributes defined for the factory and should return an array of attributes to modify: -->
상태 변환 메서드는 일반적으로 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리에 정의된 원시 속성 배열을 전달받는 클로저를 인수로 받으며, 수정할 속성 배열을 반환해야 합니다.

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
<!-- #### "Trashed" State -->
#### "Trashed" State

<!-- If your Eloquent model can be [soft deleted](/docs/master/eloquent#soft-deleting), you may invoke the built-in `trashed` state method to indicate that the created model should already be "soft deleted". You do not need to manually define the `trashed` state as it is automatically available to all factories: -->
Eloquent 모델이 [soft deleted](/docs/master/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 이미 "소프트 삭제"된 상태여야 함을 나타낼 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 직접 정의할 필요가 없습니다.

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
<!-- ### Factory Callbacks -->
### Factory Callbacks

<!-- Factory callbacks are registered using the `afterMaking` and `afterCreating` methods and allow you to perform additional tasks after making or creating a model. You should register these callbacks by defining a `configure` method on your factory class. This method will be automatically called by Laravel when the factory is instantiated: -->
팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록하며, 모델을 만들거나 생성한 뒤 추가 작업을 수행할 수 있게 해줍니다. 이러한 콜백은 팩토리 클래스에 `configure` 메서드를 정의하여 등록해야 합니다. 이 메서드는 팩토리가 인스턴스화될 때 Laravel에 의해 자동으로 호출됩니다.

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

<!-- You may also register factory callbacks within state methods to perform additional tasks that are specific to a given state: -->
특정 상태에 필요한 추가 작업을 수행하기 위해 상태 메서드 안에서 팩토리 콜백을 등록할 수도 있습니다.

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
<!-- ## Creating Models Using Factories -->
## Creating Models Using Factories

<a name="instantiating-models"></a>
<!-- ### Instantiating Models -->
### Instantiating Models

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. Let's take a look at a few examples of creating models. First, we'll use the `make` method to create models without persisting them to the database: -->
팩토리를 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` trait이 모델에 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다. 모델을 생성하는 몇 가지 예시를 살펴보겠습니다. 먼저 `make` 메서드를 사용하여 모델을 데이터베이스에 저장하지 않고 생성해 보겠습니다.

```php
use App\Models\User;

$user = User::factory()->make();
```

<!-- You may create a collection of many models using the `count` method: -->
`count` 메서드를 사용하여 여러 모델로 이루어진 컬렉션을 생성할 수 있습니다.

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
<!-- #### Applying States -->
#### Applying States

<!-- You may also apply any of your [states](#factory-states) to the models. If you would like to apply multiple state transformations to the models, you may simply call the state transformation methods directly: -->
모델에 [states](#factory-states)를 적용할 수도 있습니다. 모델에 여러 상태 변환을 적용하려면 상태 변환 메서드를 직접 연달아 호출하면 됩니다.

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
<!-- #### Overriding Attributes -->
#### Overriding Attributes

<!-- If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified attributes will be replaced while the rest of the attributes remain set to their default values as specified by the factory: -->
모델의 일부 기본값을 재정의하려면 값 배열을 `make` 메서드에 전달할 수 있습니다. 지정한 속성만 교체되며, 나머지 속성은 팩토리에 지정된 기본값 그대로 유지됩니다.

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

<!-- Alternatively, the `state` method may be called directly on the factory instance to perform an inline state transformation: -->
또는 팩토리 인스턴스에서 `state` 메서드를 직접 호출하여 인라인 상태 변환을 수행할 수 있습니다.

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용해 모델을 생성할 때는 [Mass assignment protection](/docs/master/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
<!-- ### Persisting Models -->
### Persisting Models

<!-- The `create` method instantiates model instances and persists them to the database using Eloquent's `save` method: -->
`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 사용하여 데이터베이스에 저장합니다.

```php
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```

<!-- You may override the factory's default model attributes by passing an array of attributes to the `create` method: -->
속성 배열을 `create` 메서드에 전달하여 팩토리의 기본 모델 속성을 재정의할 수 있습니다.

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
<!-- ### Sequences -->
### Sequences

<!-- Sometimes you may wish to alternate the value of a given model attribute for each created model. You may accomplish this by defining a state transformation as a sequence. For example, you may wish to alternate the value of an `admin` column between `Y` and `N` for each created user: -->
생성되는 각 모델마다 특정 모델 속성의 값을 번갈아가며 설정하고 싶을 때가 있습니다. 이를 위해 상태 변환을 시퀀스로 정의할 수 있습니다. 예를 들어 생성되는 각 사용자마다 `admin` 컬럼 값을 `Y`와 `N` 사이에서 번갈아 설정하고 싶을 수 있습니다.

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

<!-- In this example, five users will be created with an `admin` value of `Y` and five users will be created with an `admin` value of `N`. -->
이 예시에서는 `admin` 값이 `Y`인 사용자 5명과 `admin` 값이 `N`인 사용자 5명이 생성됩니다.

<!-- If necessary, you may include a closure as a sequence value. The closure will be invoked each time the sequence needs a new value: -->
필요하다면 시퀀스 값으로 클로저를 포함할 수도 있습니다. 시퀀스에 새 값이 필요할 때마다 클로저가 호출됩니다.

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

<!-- Within a sequence closure, you may access the `$index` property on the sequence instance that is injected into the closure. The `$index` property contains the number of iterations through the sequence that have occurred thus far: -->
시퀀스 클로저 안에서는 클로저에 주입되는 시퀀스 인스턴스의 `$index` 속성에 접근할 수 있습니다. `$index` 속성에는 지금까지 시퀀스를 반복한 횟수가 들어 있습니다.

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

<!-- For convenience, sequences may also be applied using the `sequence` method, which simply invokes the `state` method internally. The `sequence` method accepts a closure or arrays of sequenced attributes: -->
편의를 위해 시퀀스는 내부적으로 `state` 메서드를 호출하는 `sequence` 메서드를 사용해서도 적용할 수 있습니다. `sequence` 메서드는 클로저 또는 순서가 있는 속성 배열을 인수로 받습니다.

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
<!-- ## Factory Relationships -->
## Factory Relationships

<a name="has-many-relationships"></a>
<!-- ### Has Many Relationships -->
### Has Many Relationships

<!-- Next, let's explore building Eloquent model relationships using Laravel's fluent factory methods. First, let's assume our application has an `App\Models\User` model and an `App\Models\Post` model. Also, let's assume that the `User` model defines a `hasMany` relationship with `Post`. We can create a user that has three posts using the `has` method provided by the Laravel's factories. The `has` method accepts a factory instance: -->
다음으로 Laravel의 유창한 팩토리 메서드를 사용하여 Eloquent 모델 연관관계를 구성하는 방법을 살펴보겠습니다. 먼저 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정하겠습니다. 또한 `User` 모델이 `Post`와의 `hasMany` 연관관계를 정의한다고 가정하겠습니다. Laravel 팩토리가 제공하는 `has` 메서드를 사용하면 게시글 세 개를 가진 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인수로 받습니다.

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

<!-- By convention, when passing a `Post` model to the `has` method, Laravel will assume that the `User` model must have a `posts` method that defines the relationship. If necessary, you may explicitly specify the name of the relationship that you would like to manipulate: -->
규칙에 따라 `Post` 모델을 `has` 메서드에 전달하면, Laravel은 `User` 모델에 연관관계를 정의하는 `posts` 메서드가 있어야 한다고 가정합니다. 필요하다면 조작하려는 연관관계의 이름을 명시적으로 지정할 수 있습니다.

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

<!-- Of course, you may perform state manipulations on the related models. In addition, you may pass a closure-based state transformation if your state change requires access to the parent model: -->
물론 연관된 모델에 상태 조작을 수행할 수도 있습니다. 또한 상태 변경에 부모 모델 접근이 필요하다면 클로저 기반 상태 변환을 전달할 수 있습니다.

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
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to build relationships. For example, the following example will use convention to determine that the related models should be created via a `posts` relationship method on the `User` model: -->
편의를 위해 Laravel의 매직 팩토리 연관관계 메서드를 사용하여 연관관계를 구성할 수 있습니다. 예를 들어 다음 예시는 규칙을 사용하여 관련 모델이 `User` 모델의 `posts` 연관관계 메서드를 통해 생성되어야 한다고 판단합니다.

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```
<!-- When using magic methods to create factory relationships, you may pass an array of attributes to override on the related models: -->
매직 메서드로 factory 연관관계를 만들 때, 관련 모델에서 재정의할 속성 배열을 전달할 수 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

<!-- You may provide a closure-based state transformation if your state change requires access to the parent model: -->
상태 변경에 부모 모델 접근이 필요하다면 클로저 기반 상태 변환을 제공할 수 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
<!-- ### Belongs To Relationships -->
### Belongs To Relationships

<!-- Now that we have explored how to build "has many" relationships using factories, let's explore the inverse of the relationship. The `for` method may be used to define the parent model that factory created models belong to. For example, we can create three `App\Models\Post` model instances that belong to a single user: -->
factory를 사용해 "has many" 연관관계를 만드는 방법을 살펴보았으니, 이제 그 반대 방향의 연관관계를 살펴보겠습니다. `for` 메서드는 factory가 생성한 모델이 속하게 될 부모 모델을 정의하는 데 사용할 수 있습니다. 예를 들어, 하나의 사용자에 속하는 세 개의 `App\Models\Post` 모델 인스턴스를 만들 수 있습니다.

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

<!-- If you already have a parent model instance that should be associated with the models you are creating, you may pass the model instance to the `for` method: -->
생성하려는 모델과 연결해야 하는 부모 모델 인스턴스가 이미 있다면, 그 모델 인스턴스를 `for` 메서드에 전달할 수 있습니다.

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to define "belongs to" relationships. For example, the following example will use convention to determine that the three posts should belong to the `user` relationship on the `Post` model: -->
편의를 위해 Laravel의 매직 factory 연관관계 메서드를 사용하여 "belongs to" 연관관계를 정의할 수 있습니다. 예를 들어, 다음 예제는 관례를 사용하여 세 개의 게시글이 `Post` 모델의 `user` 연관관계에 속해야 한다고 판단합니다.

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
<!-- ### Many to Many Relationships -->
### Many to Many Relationships

<!-- Like [has many relationships](#has-many-relationships), "many to many" relationships may be created using the `has` method: -->
[has many relationships](#has-many-relationships)와 마찬가지로, "many to many" 연관관계도 `has` 메서드를 사용하여 만들 수 있습니다.

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
<!-- #### Pivot Table Attributes -->
#### Pivot Table Attributes

<!-- If you need to define attributes that should be set on the pivot / intermediate table linking the models, you may use the `hasAttached` method. This method accepts an array of pivot table attribute names and values as its second argument: -->
모델을 연결하는 pivot / 중간 테이블에 설정할 속성을 정의해야 한다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수로 pivot 테이블 속성 이름과 값의 배열을 받습니다.

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

<!-- You may provide a closure-based state transformation if your state change requires access to the related model: -->
상태 변경에 관련 모델 접근이 필요하다면 클로저 기반 상태 변환을 제공할 수 있습니다.

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

<!-- If you already have model instances that you would like to be attached to the models you are creating, you may pass the model instances to the `hasAttached` method. In this example, the same three roles will be attached to all three users: -->
생성하려는 모델에 첨부할 모델 인스턴스가 이미 있다면, 그 모델 인스턴스를 `hasAttached` 메서드에 전달할 수 있습니다. 이 예제에서는 동일한 세 개의 역할이 세 명의 사용자 모두에게 첨부됩니다.

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to define many to many relationships. For example, the following example will use convention to determine that the related models should be created via a `roles` relationship method on the `User` model: -->
편의를 위해 Laravel의 매직 factory 연관관계 메서드를 사용하여 다대다 연관관계를 정의할 수 있습니다. 예를 들어, 다음 예제는 관례를 사용하여 관련 모델이 `User` 모델의 `roles` 연관관계 메서드를 통해 생성되어야 한다고 판단합니다.

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
<!-- ### Polymorphic Relationships -->
### Polymorphic Relationships

<!-- [Polymorphic relationships](/docs/master/eloquent-relationships#polymorphic-relationships) may also be created using factories. Polymorphic "morph many" relationships are created in the same way as typical "has many" relationships. For example, if an `App\Models\Post` model has a `morphMany` relationship with an `App\Models\Comment` model: -->
[Polymorphic relationships](/docs/master/eloquent-relationships#polymorphic-relationships)도 factory를 사용하여 만들 수 있습니다. 다형성 "morph many" 연관관계는 일반적인 "has many" 연관관계와 같은 방식으로 생성됩니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 연관관계를 가진다면 다음과 같이 사용할 수 있습니다.

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
<!-- #### Morph To Relationships -->
#### Morph To Relationships

<!-- Magic methods may not be used to create `morphTo` relationships. Instead, the `for` method must be used directly and the name of the relationship must be explicitly provided. For example, imagine that the `Comment` model has a `commentable` method that defines a `morphTo` relationship. In this situation, we may create three comments that belong to a single post by using the `for` method directly: -->
매직 메서드는 `morphTo` 연관관계를 만드는 데 사용할 수 없습니다. 대신 `for` 메서드를 직접 사용해야 하며, 연관관계 이름을 명시적으로 제공해야 합니다. 예를 들어, `Comment` 모델에 `morphTo` 연관관계를 정의하는 `commentable` 메서드가 있다고 가정해 보겠습니다. 이런 경우 `for` 메서드를 직접 사용하여 하나의 게시글에 속하는 세 개의 댓글을 만들 수 있습니다.

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
<!-- #### Polymorphic Many to Many Relationships -->
#### Polymorphic Many to Many Relationships

<!-- Polymorphic "many to many" (`morphToMany` / `morphedByMany`) relationships may be created just like non-polymorphic "many to many" relationships: -->
다형성 "many to many" (`morphToMany` / `morphedByMany`) 연관관계는 비다형성 "many to many" 연관관계와 같은 방식으로 만들 수 있습니다.

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

<!-- Of course, the magic `has` method may also be used to create polymorphic "many to many" relationships: -->
물론 매직 `has` 메서드를 사용해서도 다형성 "many to many" 연관관계를 만들 수 있습니다.

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
<!-- ### Defining Relationships Within Factories -->
### Defining Relationships Within Factories

<!-- To define a relationship within your model factory, you will typically assign a new factory instance to the foreign key of the relationship. This is normally done for the "inverse" relationships such as `belongsTo` and `morphTo` relationships. For example, if you would like to create a new user when creating a post, you may do the following: -->
모델 factory 안에서 연관관계를 정의하려면 일반적으로 연관관계의 외래 키에 새 factory 인스턴스를 할당합니다. 이는 보통 `belongsTo` 및 `morphTo` 연관관계처럼 "역방향" 연관관계에 사용됩니다. 예를 들어, 게시글을 만들 때 새 사용자도 함께 만들고 싶다면 다음과 같이 할 수 있습니다.

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

<!-- If the relationship's columns depend on the factory that defines it you may assign a closure to an attribute. The closure will receive the factory's evaluated attribute array: -->
연관관계의 컬럼이 이를 정의하는 factory에 의존한다면, 속성에 클로저를 할당할 수 있습니다. 이 클로저는 factory가 평가한 속성 배열을 받습니다.

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
<!-- ### Recycling an Existing Model for Relationships -->
### Recycling an Existing Model for Relationships

<!-- If you have models that share a common relationship with another model, you may use the `recycle` method to ensure a single instance of the related model is recycled for all of the relationships created by the factory. -->
다른 모델과 공통 연관관계를 공유하는 모델들이 있다면, `recycle` 메서드를 사용하여 factory가 생성하는 모든 연관관계에서 관련 모델의 단일 인스턴스를 재사용하도록 할 수 있습니다.

<!-- For example, imagine you have `Airline`, `Flight`, and `Ticket` models, where the ticket belongs to an airline and a flight, and the flight also belongs to an airline. When creating tickets, you will probably want the same airline for both the ticket and the flight, so you may pass an airline instance to the `recycle` method: -->
예를 들어 `Airline`, `Flight`, `Ticket` 모델이 있다고 가정해 보겠습니다. 티켓은 항공사와 항공편에 속하고, 항공편도 항공사에 속합니다. 티켓을 만들 때는 티켓과 항공편 모두에 같은 항공사를 사용하고 싶을 가능성이 높으므로, 항공사 인스턴스를 `recycle` 메서드에 전달할 수 있습니다.

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

<!-- You may find the `recycle` method particularly useful if you have models belonging to a common user or team. -->
공통 사용자나 팀에 속하는 모델이 있다면 `recycle` 메서드가 특히 유용할 수 있습니다.

<!-- The `recycle` method also accepts a collection of existing models. When a collection is provided to the `recycle` method, a random model from the collection will be chosen when the factory needs a model of that type: -->
`recycle` 메서드는 기존 모델 컬렉션도 받을 수 있습니다. `recycle` 메서드에 컬렉션을 제공하면, factory가 해당 타입의 모델을 필요로 할 때 컬렉션에서 임의의 모델 하나가 선택됩니다.

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
