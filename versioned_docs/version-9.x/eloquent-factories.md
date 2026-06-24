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
    - [Many To Many Relationships](#many-to-many-relationships)
    - [Polymorphic Relationships](#polymorphic-relationships)
    - [Defining Relationships Within Factories](#defining-relationships-within-factories)
    - [Recycling An Existing Model For Relationships](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When testing your application or seeding your database, you may need to insert a few records into your database. Instead of manually specifying the value of each column, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/9.x/eloquent) using model factories. -->
애플리케이션을 테스트하거나 데이터베이스 시딩을 할 때, 데이터베이스에 여러 레코드를 삽입해야 할 경우가 있습니다. 모든 컬럼 값을 직접 지정하지 않고, Laravel에서는 각 [Eloquent models](/docs/9.x/eloquent)에 대해 모델 팩토리를 통해 기본 속성 집합을 정의할 수 있도록 지원합니다.

<!-- To see an example of how to write a factory, take a look at the `database/factories/UserFactory.php` file in your application. This factory is included with all new Laravel applications and contains the following factory definition: -->
팩토리를 작성하는 방법을 알고 싶다면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본으로 포함되어 있으며, 다음과 같이 팩토리가 정의되어 있습니다.

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
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

<!-- As you can see, in their most basic form, factories are classes that extend Laravel's base factory class and define a `definition` method. The `definition` method returns the default set of attribute values that should be applied when creating a model using the factory. -->
보시다시피, 팩토리는 가장 기본적으로 Laravel의 기본 팩토리 클래스를 상속하고 `definition` 메서드를 정의하는 클래스입니다. 이 `definition` 메서드는 팩토리를 통해 모델을 생성할 때 적용될 속성 값들의 기본 셋을 반환합니다.

<!-- Via the `fake` helper, factories have access to the [Faker](https://github.com/FakerPHP/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing and seeding. -->
팩토리에서는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있으며, 이를 이용해 테스트와 시딩에 유용한 다양한 종류의 임의 데이터를 간편하게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 로케일은 `config/app.php` 설정 파일에 `faker_locale` 옵션을 추가하여 지정할 수 있습니다.

<a name="defining-model-factories"></a>
<!-- ## Defining Model Factories -->
## Defining Model Factories

<a name="generating-factories"></a>
<!-- ### Generating Factories -->
### Generating Factories

<!-- To create a factory, execute the `make:factory` [Artisan command](/docs/9.x/artisan): -->
팩토리를 생성하려면, `make:factory` [Artisan command](/docs/9.x/artisan)를 실행합니다.

```shell
php artisan make:factory PostFactory
```

<!-- The new factory class will be placed in your `database/factories` directory. -->
새롭게 생성된 팩토리 클래스는 `database/factories` 디렉토리에 위치하게 됩니다.

<a name="factory-and-model-discovery-conventions"></a>
<!-- #### Model & Factory Discovery Conventions -->
#### Model & Factory Discovery Conventions

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. -->
팩토리를 정의한 후에는, 해당 모델에서 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇이 제공하는 정적 `factory` 메서드를 사용하여 팩토리 인스턴스를 생성할 수 있습니다.

<!-- The `HasFactory` trait's `factory` method will use conventions to determine the proper factory for the model the trait is assigned to. Specifically, the method will look for a factory in the `Database\Factories` namespace that has a class name matching the model name and is suffixed with `Factory`. If these conventions do not apply to your particular application or factory, you may overwrite the `newFactory` method on your model to return an instance of the model's corresponding factory directly: -->
`HasFactory` 트레잇의 `factory` 메서드는 해당 트레잇이 할당된 모델에 맞는 팩토리를 규약에 따라 자동으로 찾습니다. 구체적으로, `Database\Factories` 네임스페이스 아래에서 모델명과 동일하면서 `Factory`로 끝나는 클래스명을 가진 팩토리를 찾게 됩니다. 만약 이러한 규약이 애플리케이션이나 팩토리에 맞지 않으면, 모델에서 `newFactory` 메서드를 오버라이드하여 해당 모델과 매칭되는 팩토리 인스턴스를 직접 반환할 수 있습니다.

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
그리고 해당 팩토리 클래스에 `model` 속성을 정의해야 합니다.

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
상태(States) 조작 메서드를 사용하면, 모델 팩토리의 속성 값을 다양한 조합으로 선택적으로 수정할 수 있습니다. 예를 들어, `Database\Factories\UserFactory`에서 기본 속성 값을 변경하는 `suspended` 상태 메서드를 추가할 수 있습니다.

<!-- State transformation methods typically call the `state` method provided by Laravel's base factory class. The `state` method accepts a closure which will receive the array of raw attributes defined for the factory and should return an array of attributes to modify: -->
상태 변환 메서드는 주로 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출하여 구현합니다. `state` 메서드는 현재 팩토리의 원시 속성 배열을 파라미터로 전달하는 클로저를 인자로 받으며, 변경할 속성 배열을 반환해야 합니다.

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

<!-- #### "Trashed" State -->
#### "Trashed" State

<!-- If your Eloquent model can be [soft deleted](/docs/9.x/eloquent#soft-deleting), you may invoke the built-in `trashed` state method to indicate that the created model should already be "soft deleted". You do not need to manually define the `trashed` state as it is automatically available to all factories: -->
Eloquent 모델이 [soft deleted](/docs/9.x/eloquent#soft-deleting)를 지원한다면, 생성된 모델을 "소프트 삭제" 상태로 만들기 위해 내장된 `trashed` 상태 메서드를 사용할 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 별도로 정의할 필요가 없습니다.

```
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
<!-- ### Factory Callbacks -->
### Factory Callbacks

<!-- Factory callbacks are registered using the `afterMaking` and `afterCreating` methods and allow you to perform additional tasks after making or creating a model. You should register these callbacks by defining a `configure` method on your factory class. This method will be automatically called by Laravel when the factory is instantiated: -->
팩토리 콜백은 `afterMaking`과 `afterCreating` 메서드를 사용해 등록할 수 있으며, 모델을 생성(make)하거나 저장(create)한 후 추가 작업을 할 수 있게 해줍니다. 이러한 콜백들은 팩토리 클래스 안에 `configure` 메서드를 정의함으로써 등록할 수 있습니다. Laravel은 팩토리 인스턴스를 생성할 때 자동으로 이 메서드를 호출합니다.

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
팩토리를 정의한 후에는, 해당 모델에서 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇이 제공하는 정적 `factory` 메서드를 사용해 팩토리 인스턴스를 생성할 수 있습니다. 실제로 모델을 생성하는 몇 가지 예시를 살펴보겠습니다. 먼저, `make` 메서드를 사용하면 데이터베이스에 저장하지 않고 모델을 인스턴스화할 수 있습니다.

```
use App\Models\User;

$user = User::factory()->make();
```

<!-- You may create a collection of many models using the `count` method: -->
`count` 메서드를 사용하면 여러 개의 모델 컬렉션을 한 번에 만들 수 있습니다.

```
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
<!-- #### Applying States -->
#### Applying States

<!-- You may also apply any of your [states](#factory-states) to the models. If you would like to apply multiple state transformations to the models, you may simply call the state transformation methods directly: -->
모델을 생성할 때, 원하는 [states](#factory-states)를 적용할 수도 있습니다. 여러 상태 변환을 동시에 적용하고 싶다면, 해당 상태 메서드를 연속적으로 호출하면 됩니다.

```
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
<!-- #### Overriding Attributes -->
#### Overriding Attributes

<!-- If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified attributes will be replaced while the rest of the attributes remain set to their default values as specified by the factory: -->
기본 속성 값 중 일부만 변경하고 싶을 때는, 원하는 속성 배열을 `make` 메서드에 전달하면 됩니다. 지정한 속성만 덮어써지고, 나머지는 팩토리에 정의된 기본값이 사용됩니다.

```
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

<!-- Alternatively, the `state` method may be called directly on the factory instance to perform an inline state transformation: -->
또는, 팩토리 인스턴스에 직접 `state` 메서드를 호출해 인라인 상태 변환을 할 수 있습니다.

```
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용할 때는 [Mass assignment protection](/docs/9.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
<!-- ### Persisting Models -->
### Persisting Models

<!-- The `create` method instantiates model instances and persists them to the database using Eloquent's `save` method: -->
`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다.

```
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```

<!-- You may override the factory's default model attributes by passing an array of attributes to the `create` method: -->
마찬가지로, `create` 메서드에 속성 배열을 전달해 기본 속성 값을 오버라이드할 수 있습니다.

```
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
<!-- ### Sequences -->
### Sequences

<!-- Sometimes you may wish to alternate the value of a given model attribute for each created model. You may accomplish this by defining a state transformation as a sequence. For example, you may wish to alternate the value of an `admin` column between `Y` and `N` for each created user: -->
여러 개의 모델을 생성할 때, 각 모델의 특정 속성 값을 번갈아가며 다르게 지정하고 싶을 때가 있습니다. 이런 경우, 상태 변환을 시퀀스(Sequence)로 정의할 수 있습니다. 예를 들어, 생성되는 사용자마다 `admin` 컬럼 값을 번갈아가며 `Y`와 `N`으로 지정하려면 다음과 같이 할 수 있습니다.

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
이 예시에서는 5명의 사용자는 `admin` 값이 `Y`로 생성되고, 나머지 5명은 `admin` 값이 `N`으로 생성됩니다.

<!-- If necessary, you may include a closure as a sequence value. The closure will be invoked each time the sequence needs a new value: -->
필요하다면, 시퀀스 값으로 클로저를 사용할 수도 있습니다. 이 클로저는 시퀀스가 새 값을 필요로 할 때마다 호출됩니다.

```
$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn ($sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

<!-- Within a sequence closure, you may access the `$index` or `$count` properties on the sequence instance that is injected into the closure. The `$index` property contains the number of iterations through the sequence that have occurred thus far, while the `$count` property contains the total number of times the sequence will be invoked: -->
시퀀스 클로저 안에서는, 시퀀스 인스턴스에 주입된 `$index`나 `$count` 속성을 사용할 수 있습니다. `$index`는 지금까지 시퀀스가 반복된 횟수를, `$count`는 시퀀스가 호출될 총 횟수를 나타냅니다.

```
$users = User::factory()
                ->count(10)
                ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

<!-- For convenience, sequences may also be applied using the `sequence` method, which simply invokes the `state` method internally. The `sequence` method accepts a closure or arrays of sequenced attributes: -->
편의상, 시퀀스는 `sequence` 메서드를 이용해 적용할 수도 있습니다. 이 메서드는 내부적으로 `state` 메서드를 호출합니다. `sequence` 메서드는 클로저나, 순차적으로 적용할 속성들의 배열을 받을 수 있습니다.

```
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
이제 Laravel의 플루언트 팩토리 메서드를 사용해 Eloquent 모델의 관계를 만들어보겠습니다. 먼저, 애플리케이션에 `App\Models\User`와 `App\Models\Post` 모델이 있다고 가정하겠습니다. 또한, `User` 모델이 `Post`와 `hasMany` 관계를 정의한다고 할 때, 사용자가 3개의 포스트를 가지게 하려면 팩토리의 `has` 메서드를 이용할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인자로 받습니다.

```
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

<!-- By convention, when passing a `Post` model to the `has` method, Laravel will assume that the `User` model must have a `posts` method that defines the relationship. If necessary, you may explicitly specify the name of the relationship that you would like to manipulate: -->
관례상, `Post` 모델을 `has` 메서드에 전달하면, Laravel은 `User` 모델에 반드시 `posts` 메서드가 있어야 한다고 가정합니다. 만약 조작하려는 관계명을 명시하고 싶다면 두 번째 인자로 관계 이름을 지정할 수 있습니다.

```
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

<!-- Of course, you may perform state manipulations on the related models. In addition, you may pass a closure based state transformation if your state change requires access to the parent model: -->
물론, 관계 모델에도 상태 변경을 적용할 수 있습니다. 부모 모델 데이터에 따라 관계 모델의 속성을 변경하려면, 클로저를 이용한 상태 변환을 전달할 수 있습니다.

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
더 간편하게 팩토리 관계를 설정하고 싶다면, Laravel의 매직 팩토리 관계 메서드를 사용할 수 있습니다. 아래 예시는 `User` 모델에 `posts` 관계 메서드가 있다고 가정하고, 관례에 따라 관련 모델을 생성합니다.

```
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

<!-- When using magic methods to create factory relationships, you may pass an array of attributes to override on the related models: -->
매직 메서드를 사용할 때도, 관계 모델의 속성 값을 오버라이드할 수 있도록 배열을 전달할 수 있습니다.

```
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

<!-- You may provide a closure based state transformation if your state change requires access to the parent model: -->
부모 모델 정보를 바탕으로 관계 모델의 속성을 바꿔야 한다면 클로저를 전달할 수도 있습니다.

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
"Has many" 관계를 팩토리로 만드는 방법을 살펴봤으니, 이제 그 반대 관계도 알아보겠습니다. `for` 메서드를 사용하면 팩토리가 생성하는 모델이 어떤 부모 모델에 속하는지를 지정할 수 있습니다. 예를 들어, `App\Models\Post` 모델 인스턴스 3개를 생성하면서, 이들이 모두 하나의 사용자에 속하도록 할 수 있습니다.

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
이미 생성된 부모 모델 인스턴스가 있다면, 이를 `for` 메서드에 그대로 전달해 관계를 지정할 수 있습니다.

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
편리하게 "belongs to" 관계를 지정하고 싶다면, Laravel의 매직 팩토리 메서드를 사용할 수 있습니다. 예를 들어 아래 예시는 3개의 포스트가 모두 `Post` 모델의 `user` 관계에 속하게 생성됩니다.

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
[has many relationships](#has-many-relationships)와 마찬가지로, "many to many" 관계도 `has` 메서드를 이용해 생성할 수 있습니다.

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
모델 사이를 연결하는 pivot(중간) 테이블에 추가 속성을 지정하고 싶을 때는, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인자로 pivot 테이블에 설정할 속성들의 배열을 받습니다.

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
관계된 모델 정보를 활용해 상태를 동적으로 지정하고 싶을 때는, 클로저를 이용한 상태 변환을 넘길 수 있습니다.

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
이미 생성된 모델 인스턴스를 관계에 사용할 경우, `hasAttached` 메서드에 그 인스턴스들을 넘길 수 있습니다. 아래 예시처럼 세 개의 역할(role)이 각각 세 명의 사용자에 모두 연결됩니다.

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
다대다 관계를 더욱 쉽게 정의하려면, Laravel의 매직 팩토리 메서드를 사용할 수 있습니다. 아래 예시는 `User` 모델의 `roles` 관계를 통해 관련 모델을 생성합니다.

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

<!-- [Polymorphic relationships](/docs/9.x/eloquent-relationships#polymorphic-relationships) may also be created using factories. Polymorphic "morph many" relationships are created in the same way as typical "has many" relationships. For example, if a `App\Models\Post` model has a `morphMany` relationship with a `App\Models\Comment` model: -->
[Polymorphic relationships](/docs/9.x/eloquent-relationships#polymorphic-relationships)도 팩토리를 이용해 만들 수 있습니다. 폴리모픽 "morph many" 관계는 일반적인 "has many" 관계와 동일한 방식으로 생성합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가진다면 다음과 같이 생성 가능합니다.

```
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
<!-- #### Morph To Relationships -->
#### Morph To Relationships

<!-- Magic methods may not be used to create `morphTo` relationships. Instead, the `for` method must be used directly and the name of the relationship must be explicitly provided. For example, imagine that the `Comment` model has a `commentable` method that defines a `morphTo` relationship. In this situation, we may create three comments that belong to a single post by using the `for` method directly: -->
`morphTo` 관계를 생성할 때는 매직 메서드를 사용할 수 없습니다. 대신, `for` 메서드를 직접 사용하며, 관계 명을 명시적으로 지정해야 합니다. 예를 들어, `Comment` 모델에 `morphTo` 관계를 정의하는 `commentable` 메서드가 있다면, `for` 메서드를 직접 사용하여 하나의 포스트에 속한 댓글 3개를 생성할 수 있습니다.

```
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
<!-- #### Polymorphic Many To Many Relationships -->
#### Polymorphic Many To Many Relationships

<!-- Polymorphic "many to many" (`morphToMany` / `morphedByMany`) relationships may be created just like non-polymorphic "many to many" relationships: -->
폴리모픽 "many to many"(`morphToMany` / `morphedByMany`) 관계 역시 일반 다대다 관계와 마찬가지로 생성할 수 있습니다.

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
물론, 매직 `has` 메서드를 사용해서도 폴리모픽 다대다 관계를 생성할 수 있습니다.

```
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
<!-- ### Defining Relationships Within Factories -->
### Defining Relationships Within Factories

<!-- To define a relationship within your model factory, you will typically assign a new factory instance to the foreign key of the relationship. This is normally done for the "inverse" relationships such as `belongsTo` and `morphTo` relationships. For example, if you would like to create a new user when creating a post, you may do the following: -->
팩토리 내부에서 관계를 정의할 때는, 보통 외래 키(foreign key)에 새 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo`나 `morphTo` 같은 "역방향" 관계에 적용됩니다. 예를 들어, 포스트를 생성할 때 새 사용자를 함께 생성하고 싶다면 아래와 같이 작업할 수 있습니다.

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
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<!-- If the relationship's columns depend on the factory that defines it you may assign a closure to an attribute. The closure will receive the factory's evaluated attribute array: -->
관계의 컬럼 값이 팩토리에서 정의된 데이터에 따라 달라져야 할 때는, 속성에 클로저를 할당할 수도 있습니다. 이때 클로저에는 팩토리에서 평가된 속성 배열이 전달됩니다.

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
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a name="recycling-an-existing-model-for-relationships"></a>
<!-- ### Recycling An Existing Model For Relationships -->
### Recycling An Existing Model For Relationships

<!-- If you have models that share a common relationship with another model, you may use the `recycle` method to ensure a single instance of the related model is recycled for all of the relationships created by the factory. -->
공통된 관계 모델을 여러 개의 모델이 공유해야 한다면, `recycle` 메서드를 사용해 모든 관계에서 동일한 모델 인스턴스를 재사용할 수 있습니다.

<!-- For example, imagine you have `Airline`, `Flight`, and `Ticket` models, where the ticket belongs to an airline and a flight, and the flight also belongs to an airline. When creating tickets, you will probably want the same airline for both the ticket and the flight, so you may pass an airline instance to the `recycle` method: -->
예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 항공편 각각에 속하며, 항공편 또한 항공사에 속한다고 가정해봅시다. 티켓을 생성할 때, 티켓과 항공편 모두 동일한 항공사를 사용하려면 `recycle` 메서드로 같은 항공사 인스턴스를 전달하면 됩니다.

```
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

<!-- You may find the `recycle` method particularly useful if you have models belonging to a common user or team. -->
특히 여러 모델이 공통 사용자나 팀에 속할 때, `recycle` 메서드는 매우 유용합니다.

<!-- The `recycle` method also accepts a collection of existing models. When a collection is provided to the `recycle` method, a random model from the collection will be chosen when the factory needs a model of that type: -->
`recycle` 메서드는 기존 모델의 컬렉션도 인자로 받을 수 있습니다. 컬렉션이 `recycle` 메서드에 주어지면, 팩토리가 해당 타입의 모델이 필요할 때마다 컬렉션에서 임의의 모델 하나를 선택해서 사용하게 됩니다.

```
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
