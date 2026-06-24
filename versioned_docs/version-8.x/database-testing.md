<!-- # Database Testing -->
# Database Testing

- [Introduction](#introduction)
    - [Resetting The Database After Each Test](#resetting-the-database-after-each-test)
- [Defining Model Factories](#defining-model-factories)
    - [Concept Overview](#concept-overview)
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
    - [Many To Many Relationships](#many-to-many-relationships)
    - [Polymorphic Relationships](#polymorphic-relationships)
    - [Defining Relationships Within Factories](#defining-relationships-within-factories)
- [Running Seeders](#running-seeders)
- [Available Assertions](#available-assertions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a variety of helpful tools and assertions to make it easier to test your database driven applications. In addition, Laravel model factories and seeders make it painless to create test database records using your application's Eloquent models and relationships. We'll discuss all of these powerful features in the following documentation. -->
Laravel은 데이터베이스 기반 애플리케이션을 테스트하기 위한 다양한 유용한 도구와 assertion을 제공합니다. 또한, Eloquent 모델 팩토리와 시더(Seeder)를 사용하면 애플리케이션의 Eloquent 모델과 그 연관관계를 활용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이 문서에서는 이러한 강력한 기능들을 모두 다룹니다.

<a name="resetting-the-database-after-each-test"></a>
<!-- ### Resetting The Database After Each Test -->
### Resetting The Database After Each Test

<!-- Before proceeding much further, let's discuss how to reset your database after each of your tests so that data from a previous test does not interfere with subsequent tests. Laravel's included `Illuminate\Foundation\Testing\RefreshDatabase` trait will take care of this for you. Simply use the trait on your test class: -->
본격적으로 살펴보기 전에, 각 테스트 실행 후 데이터베이스를 초기화해 이전 테스트의 데이터가 다음 테스트에 영향을 주지 않도록 하는 방법부터 알아보겠습니다. Laravel은 `Illuminate\Foundation\Testing\RefreshDatabase` 트레잇을 제공하며, 이 트레잇을 테스트 클래스에 추가하면 알아서 데이터베이스 초기화를 처리해줍니다. 다음과 같이 테스트 클래스에 트레잇을 사용하면 됩니다.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_basic_example()
    {
        $response = $this->get('/');

        // ...
    }
}
```

<a name="defining-model-factories"></a>
<a id="writing-factories" data-translation-alias="true"></a>
<!-- ## Defining Model Factories -->
## Defining Model Factories

<a name="concept-overview"></a>
<!-- ### Concept Overview -->
### Concept Overview

<!-- First, let's talk about Eloquent model factories. When testing, you may need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/8.x/eloquent) using model factories. -->
먼저, Eloquent 모델 팩토리에 대해 알아보겠습니다. 테스트를 작성할 때, 데이터를 직접 일일이 컬럼 값으로 지정하지 않고 데이터베이스에 여러 레코드를 삽입해야 하는 경우가 자주 있습니다. 이때 Laravel의 모델 팩토리를 이용하면 각 [Eloquent models](/docs/8.x/eloquent)별로 기본 속성(attribute) 세트를 정의해놓고 필요할 때마다 간편하게 테스트 데이터를 생성할 수 있습니다.

<!-- To see an example of how to write a factory, take a look at the `database/factories/UserFactory.php` file in your application. This factory is included with all new Laravel applications and contains the following factory definition: -->
팩토리 예시를 보려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 확인해 보십시오. 이 팩토리는 모든 신규 Laravel 프로젝트에 기본 포함되어 있으며, 아래와 같은 팩토리 정의를 가지고 있습니다.

```
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'name' => $this->faker->name(),
            'email' => $this->faker->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

<!-- As you can see, in their most basic form, factories are classes that extend Laravel's base factory class and define `definition` method. The `definition` method returns the default set of attribute values that should be applied when creating a model using the factory. -->
보시다시피, 팩토리는 기본적으로 Laravel의 베이스 팩토리 클래스를 상속하며 `definition` 메서드를 정의합니다. 이 `definition` 메서드는 팩토리를 통해 모델을 생성할 때 적용할 기본 속성값 배열을 리턴합니다.

<!-- Via the `faker` property, factories have access to the [Faker](https://github.com/FakerPHP/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing. -->
팩토리의 `faker` 프로퍼티를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있기 때문에, 테스트에 활용할 다양한 무작위 데이터를 쉽게 생성할 수 있습니다.

> [!TIP]
> 애플리케이션의 Faker 언어(locale)를 변경하려면 `config/app.php` 설정 파일에 `faker_locale` 옵션을 추가하면 됩니다.

<a name="generating-factories"></a>
<!-- ### Generating Factories -->
### Generating Factories

<!-- To create a factory, execute the `make:factory` [Artisan command](/docs/8.x/artisan): -->
새로운 팩토리를 생성하려면, `make:factory` [Artisan command](/docs/8.x/artisan)를 실행합니다.

```
php artisan make:factory PostFactory
```

<!-- The new factory class will be placed in your `database/factories` directory. -->
이 명령어를 실행하면, 새로 만들어진 팩토리 클래스가 `database/factories` 디렉터리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
<!-- #### Model & Factory Discovery Conventions -->
#### Model & Factory Discovery Conventions

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. -->
팩토리를 정의했다면, 이제 모델에 포함된 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇이 제공하는 `factory` 정적 메서드를 통해 팩토리 인스턴스를 생성할 수 있습니다.

<!-- The `HasFactory` trait's `factory` method will use conventions to determine the proper factory for the model the trait is assigned to. Specifically, the method will look for a factory in the `Database\Factories` namespace that has a class name matching the model name and is suffixed with `Factory`. If these conventions do not apply to your particular application or factory, you may overwrite the `newFactory` method on your model to return an instance of the model's corresponding factory directly: -->
이때 `HasFactory` 트레잇의 `factory` 메서드는 이름 규칙(convention)에 따라 해당 모델을 위한 올바른 팩토리를 자동으로 찾아 사용합니다. 구체적으로, `Database\Factories` 네임스페이스 내에 모델명과 동일하고 `Factory`라는 접미사가 붙은 클래스를 찾습니다. 만약 이 규칙을 따를 수 없는 상황이거나 별도의 팩토리를 지정하고 싶을 때는, 모델 클래스에서 `newFactory` 메서드를 오버라이드해 직접 원하는 팩토리 인스턴스를 반환하면 됩니다.

```
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

<!-- Next, define a `model` property on the corresponding factory: -->
그리고 해당 팩토리 클래스에는 `model` 프로퍼티를 명시해줍니다:

```
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
<!-- ### Factory States -->
### Factory States

<!-- State manipulation methods allow you to define discrete modifications that can be applied to your model factories in any combination. For example, your `Database\Factories\UserFactory` factory might contain a `suspended` state method that modifies one of its default attribute values. -->
상태(state) 조작 메서드를 활용하면, 모델 팩토리에 다양한 속성 변형을 별도로 정의해 두고 자유롭게 조합해서 적용할 수 있습니다. 예를 들어, `Database\Factories\UserFactory`에서 사용자의 기본 속성을 변경하는 `suspended` 상태(state) 메서드를 아래와 같이 만들 수 있습니다.

<!-- State transformation methods typically call the `state` method provided by Laravel's base factory class. The `state` method accepts a closure which will receive the array of raw attributes defined for the factory and should return an array of attributes to modify: -->
상태 변환 메서드는 보통 Laravel의 베이스 팩토리 클래스에서 제공하는 `state` 메서드를 호출하여 작성합니다. `state` 메서드는 팩토리 기본 속성 배열을 인자로 받아, 변경할 속성값을 배열로 리턴하는 클로저를 인자로 전달받습니다.

```
/**
 * Indicate that the user is suspended.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
public function suspended()
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a name="factory-callbacks"></a>
<!-- ### Factory Callbacks -->
### Factory Callbacks

<!-- Factory callbacks are registered using the `afterMaking` and `afterCreating` methods and allow you to perform additional tasks after making or creating a model. You should register these callbacks by defining a `configure` method on your factory class. This method will be automatically called by Laravel when the factory is instantiated: -->
팩토리 콜백은 `afterMaking`, `afterCreating` 메서드를 활용해 등록할 수 있으며, 모델을 생성(메모리상 만들기)하거나 실제로 저장(데이터베이스에 생성)한 후 추가 작업을 지정할 수 있습니다. 팩토리 클래스에서 `configure` 메서드를 정의해 콜백을 등록해 주세요. 이 메서드는 팩토리 인스턴스화 시 자동으로 호출됩니다.

```
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     *
     * @return $this
     */
    public function configure()
    {
        return $this->afterMaking(function (User $user) {
            //
        })->afterCreating(function (User $user) {
            //
        });
    }

    // ...
}
```

<a name="creating-models-using-factories"></a>
<!-- ## Creating Models Using Factories -->
## Creating Models Using Factories

<a name="instantiating-models"></a>
<!-- ### Instantiating Models -->
### Instantiating Models

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. Let's take a look at a few examples of creating models. First, we'll use the `make` method to create models without persisting them to the database: -->
팩토리를 정의했으면, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇이 제공하는 `factory` 정적 메서드를 통해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다. 예시로, `make` 메서드를 사용하면 데이터베이스에 저장하지 않고 모델 객체만 생성할 수 있습니다.

```
use App\Models\User;

public function test_models_can_be_instantiated()
{
    $user = User::factory()->make();

    // Use model in tests...
}
```

<!-- You may create a collection of many models using the `count` method: -->
`count` 메서드를 사용해 여러 개의 모델 객체를 한 번에 생성할 수도 있습니다.

```
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
<!-- #### Applying States -->
#### Applying States

<!-- You may also apply any of your [states](#factory-states) to the models. If you would like to apply multiple state transformations to the models, you may simply call the state transformation methods directly: -->
원한다면, [states](#factory-states)를 하나 또는 여러 개 조합해서 적용할 수 있습니다. 아래와 같이 여러 상태 변환 메서드를 체이닝해 사용할 수 있습니다.

```
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
<!-- #### Overriding Attributes -->
#### Overriding Attributes

<!-- If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified attributes will be replaced while the rest of the attributes remain set to their default values as specified by the factory: -->
팩토리로 모델을 생성할 때, 일부 속성값만 따로 지정(overriding)하고 싶은 경우 `make` 메서드에 값을 배열로 넘기면 됩니다. 특정 값만 변경되고, 나머지 속성은 팩토리에 정의한 기본값이 적용됩니다.

```
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

<!-- Alternatively, the `state` method may be called directly on the factory instance to perform an inline state transformation: -->
또는, 팩토리 인스턴스에서 `state` 메서드를 직접 호출해 즉석에서 속성 변환을 적용할 수도 있습니다.

```
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!TIP]
> 팩토리로 모델을 생성할 때는 [Mass assignment protection](/docs/8.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
<!-- ### Persisting Models -->
### Persisting Models

<!-- The `create` method instantiates model instances and persists them to the database using Eloquent's `save` method: -->
`create` 메서드는 모델 인스턴스를 만들어 Eloquent의 `save` 메서드를 통해 데이터베이스에 바로 저장합니다.

```
use App\Models\User;

public function test_models_can_be_persisted()
{
    // Create a single App\Models\User instance...
    $user = User::factory()->create();

    // Create three App\Models\User instances...
    $users = User::factory()->count(3)->create();

    // Use model in tests...
}
```

<!-- You may override the factory's default model attributes by passing an array of attributes to the `create` method: -->
`create` 메서드에도 속성값 배열을 넘겨, 팩토리 기본값을 원하는 값으로 오버라이드할 수 있습니다.

```
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
<!-- ### Sequences -->
### Sequences

<!-- Sometimes you may wish to alternate the value of a given model attribute for each created model. You may accomplish this by defining a state transformation as a sequence. For example, you may wish to alternate the value of an `admin` column between `Y` and `N` for each created user: -->
때로는 생성하는 여러 모델 객체의 특정 속성값을 번갈아 가며 교차 지정하고 싶을 수 있습니다. 이런 경우 상태 변환을 시퀀스(sequence) 형태로 정의하면 됩니다. 예를 들어, 생성하는 사용자마다 `admin` 컬럼 값을 `Y`와 `N`으로 번갈아 설정하려면 다음과 같이 할 수 있습니다.

```
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
필요하다면, 시퀀스 값으로 클로저를 사용할 수도 있습니다. 시퀀스가 새 값을 필요로 할 때마다 클로저가 호출되어 동적으로 값을 반환할 수 있습니다.

```
$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn ($sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

<!-- Within a sequence closure, you may access the `$index` or `$count` properties on the sequence instance that is injected into the closure. The `$index` property contains the number of iterations through the sequence that have occurred thus far, while the `$count` property contains the total number of times the sequence will be invoked: -->
시퀀스 클로저 내부에서는 클로저에 주입되는 시퀀스 인스턴스의 `$index` 또는 `$count` 속성에 접근할 수 있습니다. `$index` 속성에는 현재까지 시퀀스를 거친 횟수가 담기며, `$count` 속성에는 시퀀스가 호출될 총 횟수가 담깁니다.

```
$users = User::factory()
                ->count(10)
                ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

<a name="factory-relationships"></a>
<!-- ## Factory Relationships -->
## Factory Relationships

<a name="has-many-relationships"></a>
<!-- ### Has Many Relationships -->
### Has Many Relationships

<!-- Next, let's explore building Eloquent model relationships using Laravel's fluent factory methods. First, let's assume our application has an `App\Models\User` model and an `App\Models\Post` model. Also, let's assume that the `User` model defines a `hasMany` relationship with `Post`. We can create a user that has three posts using the `has` method provided by the Laravel's factories. The `has` method accepts a factory instance: -->
이번에는 Laravel의 플루언트 팩토리 메서드를 사용해 Eloquent 모델 간 연관관계를 만드는 방법을 살펴보겠습니다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User` 모델이 `Post`와 `hasMany` 관계를 가진다고 가정해보겠습니다. Laravel 팩토리의 `has` 메서드를 사용해 하나의 사용자에 세 개의 포스트를 생성하고 연결할 수 있습니다. `has` 메서드에는 팩토리 인스턴스를 전달하면 됩니다.

```
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

<!-- By convention, when passing a `Post` model to the `has` method, Laravel will assume that the `User` model must have a `posts` method that defines the relationship. If necessary, you may explicitly specify the name of the relationship that you would like to manipulate: -->
일반적으로, `has` 메서드에 `Post` 모델을 전달하면 Laravel은 `User` 모델에 `posts`라는 관계 메서드가 있다고 간주합니다. 만약 다른 이름의 연관관계를 사용하고 싶다면, 두 번째 인자로 직접 관계명을 명시할 수도 있습니다.

```
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

<!-- Of course, you may perform state manipulations on the related models. In addition, you may pass a closure based state transformation if your state change requires access to the parent model: -->
물론, 연관된 모델에 상태 조작도 적용 가능합니다. 또한, 부모 모델을 참조해야 하는 경우에는, 클로저 기반의 상태 변환을 사용할 수도 있습니다.

```
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
편의상 Laravel의 매직 팩토리 관계 메서드도 사용할 수 있습니다. 아래 예시는 컨벤션을 이용해, 연관 모델을 `User` 모델의 `posts` 관계 메서드를 통해 생성하는 동작을 수행합니다.

```
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

<!-- When using magic methods to create factory relationships, you may pass an array of attributes to override on the related models: -->
매직 메서드를 사용할 때도 관련 모델에 적용할 속성 값을 배열로 지정할 수 있습니다.

```
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

<!-- You may provide a closure based state transformation if your state change requires access to the parent model: -->
에서처럼, 클로저 기반의 상태 변환도 사용할 수 있습니다.

```
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
1:N 관계 구축 방법을 살펴봤으니, 이제 반대 방향인 "Belongs To" 관계도 알아보겠습니다. 팩토리의 `for` 메서드를 사용해, 생성된 모델이 특정 부모 모델에 소속되도록 정의할 수 있습니다. 예를 들어, `App\Models\Post` 모델 3개를 한 명의 사용자에 소속되게 생성하는 경우입니다.

```
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
이미 부모 모델 인스턴스를 가지고 있다면, 그 객체를 직접 `for` 메서드에 넘길 수도 있습니다.

```
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
역시 편의상 "Belongs To" 관계도 Laravel 매직 팩토리 메서드를 써서 구현할 수 있습니다. 아래 예시는 규칙에 따라 3개의 포스트가 `Post` 모델의 `user` 연관관계에 소속되도록 만듭니다.

```
$posts = Post::factory()
            ->count(3)
            ->forUser([
                'name' => 'Jessica Archer',
            ])
            ->create();
```

<a name="many-to-many-relationships"></a>
<!-- ### Many To Many Relationships -->
### Many To Many Relationships

<!-- Like [has many relationships](#has-many-relationships), "many to many" relationships may be created using the `has` method: -->
[has many relationships](#has-many-relationships)와 비슷하게, 다대다(Many to Many) 관계도 팩토리의 `has` 메서드를 이용해 만들 수 있습니다.

```
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
연결 테이블(피벗 테이블)에 값을 지정해야 한다면, `hasAttached` 메서드를 사용하세요. 두 번째 인수로 피벗 테이블 속성명의 배열을 전달할 수 있습니다.

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->hasAttached(
                Role::factory()->count(3),
                ['active' => true]
            )
            ->create();
```

<!-- You may provide a closure based state transformation if your state change requires access to the related model: -->
연관된 모델을 참조해야 하는 상황에서는 클로저를 활용한 상태 변환도 사용할 수 있습니다.

```
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
이미 만들어진 모델 인스턴스를 연결하고 싶을 때는, 그 모델들을 `hasAttached`의 첫 번째 인수로 넘겨주면 됩니다. 아래 예시는 3개의 Role을 3명의 사용자 각각에 연결하는 예입니다.

```
$roles = Role::factory()->count(3)->create();

$user = User::factory()
            ->count(3)
            ->hasAttached($roles, ['active' => true])
            ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to define many to many relationships. For example, the following example will use convention to determine that the related models should be created via a `roles` relationship method on the `User` model: -->
다대다 관계 역시 매직 팩토리 메서드로 정의할 수 있습니다. 아래 예시는 `User` 모델의 `roles` 연관관계를 통해 관련 모델을 생성합니다.

```
$user = User::factory()
            ->hasRoles(1, [
                'name' => 'Editor'
            ])
            ->create();
```

<a name="polymorphic-relationships"></a>
<!-- ### Polymorphic Relationships -->
### Polymorphic Relationships

<!-- [Polymorphic relationships](/docs/8.x/eloquent-relationships#polymorphic-relationships) may also be created using factories. Polymorphic "morph many" relationships are created in the same way as typical "has many" relationships. For example, if a `App\Models\Post` model has a `morphMany` relationship with a `App\Models\Comment` model: -->
[Polymorphic relationships](/docs/8.x/eloquent-relationships#polymorphic-relationships) 또한 팩토리로 생성할 수 있습니다. 폴리모픽 "morph many" 관계 생성법은 1:N 관계와 동일합니다. 예시: `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가진 경우입니다.

```
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
<!-- #### Morph To Relationships -->
#### Morph To Relationships

<!-- Magic methods may not be used to create `morphTo` relationships. Instead, the `for` method must be used directly and the name of the relationship must be explicitly provided. For example, imagine that the `Comment` model has a `commentable` method that defines a `morphTo` relationship. In this situation, we may create three comments that belong to a single post by using the `for` method directly: -->
매직 메서드로는 `morphTo` 관계를 만들 수 없습니다. 이 경우에는 반드시 `for` 메서드를 직접 사용하고 관계명을 명시해야 합니다. 예를 들어, `Comment` 모델에 `commentable` `morphTo` 관계가 있다면, `for` 메서드를 직접 사용해 3개의 코멘트를 하나의 포스트에 소속시키는 코드는 아래와 같습니다.

```
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
<!-- #### Polymorphic Many To Many Relationships -->
#### Polymorphic Many To Many Relationships

<!-- Polymorphic "many to many" (`morphToMany` / `morphedByMany`) relationships may be created just like non-polymorphic "many to many" relationships: -->
폴리모픽 "many to many"(`morphToMany` / `morphedByMany`) 관계도 일반 다대다 관계와 동일하게 생성할 수 있습니다.

```
use App\Models\Tag;
use App\Models\Video;

$videos = Video::factory()
            ->hasAttached(
                Tag::factory()->count(3),
                ['public' => true]
            )
            ->create();
```

<!-- Of course, the magic `has` method may also be used to create polymorphic "many to many" relationships: -->
물론, `has` 매직 메서드를 사용해 폴리모픽 다대다 관계도 생성할 수 있습니다.

```
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
<!-- ### Defining Relationships Within Factories -->
### Defining Relationships Within Factories

<!-- To define a relationship within your model factory, you will typically assign a new factory instance to the foreign key of the relationship. This is normally done for the "inverse" relationships such as `belongsTo` and `morphTo` relationships. For example, if you would like to create a new user when creating a post, you may do the following: -->
팩토리 내부에서 직접 관계를 정의해야 할 때는, 보통 외래키(foreign key)에 새로운 팩토리 인스턴스를 할당하면 됩니다. 이는 대개 "inverse" 관계인 `belongsTo`나 `morphTo` 관계에서 사용합니다. 예를 들어, 포스트 작성 시 새로운 사용자를 함께 생성하려면 아래와 같이 작성합니다.

```
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array
 */
public function definition()
{
    return [
        'user_id' => User::factory(),
        'title' => $this->faker->title(),
        'content' => $this->faker->paragraph(),
    ];
}
```

<!-- If the relationship's columns depend on the factory that defines it you may assign a closure to an attribute. The closure will receive the factory's evaluated attribute array: -->
관계된 컬럼 값이 팩토리의 다른 속성에 따라 동적으로 결정되어야 한다면, 속성값에 클로저를 지정할 수도 있습니다. 이 클로저는 팩토리의 평가된 속성 배열을 인자로 받습니다.

```
/**
 * Define the model's default state.
 *
 * @return array
 */
public function definition()
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => $this->faker->title(),
        'content' => $this->faker->paragraph(),
    ];
}
```

<a name="running-seeders"></a>
<!-- ## Running Seeders -->
## Running Seeders

<!-- If you would like to use [database seeders](/docs/8.x/seeding) to populate your database during a feature test, you may invoke the `seed` method. By default, the `seed` method will execute the `DatabaseSeeder`, which should execute all of your other seeders. Alternatively, you pass a specific seeder class name to the `seed` method: -->
[database seeders](/docs/8.x/seeding)를 활용해 기능 테스트 중에 데이터베이스를 채우고 싶다면, `seed` 메서드를 호출하면 됩니다. 기본적으로 `seed` 메서드만 실행하면 `DatabaseSeeder` 클래스가 실행되어 다른 모든 시더도 자동 실행됩니다. 특정 시더만 실행하고 싶을 땐 시더 클래스명을 `seed` 메서드에 직접 넘겨주면 됩니다.

```
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Test creating a new order.
     *
     * @return void
     */
    public function test_orders_can_be_created()
    {
        // Run the DatabaseSeeder...
        $this->seed();

        // Run a specific seeder...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // Run an array of specific seeders...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

<!-- Alternatively, you may instruct Laravel to automatically seed the database before each test that uses the `RefreshDatabase` trait. You may accomplish this by defining a `$seed` property on your base test class: -->
또는, `RefreshDatabase` 트레잇을 사용하는 테스트에서 자동으로 매 테스트마다 시더가 실행되게 하려면, 베이스 테스트 클래스에 `$seed` 프로퍼티를 정의하세요.

```
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    /**
     * Indicates whether the default seeder should run before each test.
     *
     * @var bool
     */
    protected $seed = true;
}
```

<!-- When the `$seed` property is `true`, the test will run the `Database\Seeders\DatabaseSeeder` class before each test that uses the `RefreshDatabase` trait. However, you may specify a specific seeder that should be executed by defining a `$seeder` property on your test class: -->
`$seed` 프로퍼티가 `true`로 설정되어 있으면, `RefreshDatabase` 트레잇을 사용하는 각 테스트 실행 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 특정한 시더만 실행하고 싶다면, 테스트 클래스에 `$seeder` 프로퍼티를 정의하면 됩니다.

```
use Database\Seeders\OrderStatusSeeder;

/**
 * Run a specific seeder before each test.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
<!-- ## Available Assertions -->
## Available Assertions

<!-- Laravel provides several database assertions for your [PHPUnit](https://phpunit.de/) feature tests. We'll discuss each of these assertions below. -->
Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트에서 사용할 수 있는 여러 데이터베이스 assertion을 제공합니다. 각 assertion은 아래와 같습니다.

<a name="assert-database-count"></a>
<!-- #### assertDatabaseCount -->
#### assertDatabaseCount

<!-- Assert that a table in the database contains the given number of records: -->
지정한 데이터베이스 테이블에 주어진 개수의 레코드가 존재함을 확인합니다.

```
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-has"></a>
<!-- #### assertDatabaseHas -->
#### assertDatabaseHas

<!-- Assert that a table in the database contains records matching the given key / value query constraints: -->
지정한 키/값 쿼리 조건을 만족하는 레코드가 데이터베이스 테이블에 존재하는지 확인합니다.

```
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
<!-- #### assertDatabaseMissing -->
#### assertDatabaseMissing

<!-- Assert that a table in the database does not contain records matching the given key / value query constraints: -->
특정 키/값 쿼리 조건을 만족하는 레코드가 데이터베이스 테이블에 존재하지 않는지 확인합니다.

```
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
<!-- #### assertDeleted -->
#### assertDeleted

<!-- The `assertDeleted` asserts that a given Eloquent model has been deleted from the database: -->
`assertDeleted`는 지정한 Eloquent 모델이 데이터베이스에서 삭제되었는지 확인합니다.

```
use App\Models\User;

$user = User::find(1);

$user->delete();

$this->assertDeleted($user);
```

<!-- The `assertSoftDeleted` method may be used to assert a given Eloquent model has been "soft deleted": -->
`assertSoftDeleted` 메서드는 해당 Eloquent 모델이 "소프트 삭제" 처리되었는지 확인할 때 사용합니다.

```
$this->assertSoftDeleted($user);
```

<a name="assert-model-exists"></a>
<!-- #### assertModelExists -->
#### assertModelExists

<!-- Assert that a given model exists in the database: -->
지정한 모델 인스턴스가 데이터베이스에 존재하는지 확인합니다.

```
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
<!-- #### assertModelMissing -->
#### assertModelMissing

<!-- Assert that a given model does not exist in the database: -->
지정한 모델 인스턴스가 데이터베이스에 존재하지 않는지 확인합니다.

```
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```
