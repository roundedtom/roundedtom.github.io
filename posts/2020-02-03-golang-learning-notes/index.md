---
title: Golang学习笔记
author: Tom
date: "2020-02-03"
toc: true
code-block-bg: true
highlight-style: zenburn
categories:
  - Golang
image: golang.png
code-fold: false
html-math-method: katex
jupyter: python3
---

这篇博客记录 Golang 的学习笔记。

# 1 数组（array）

- 数组是一组具有相同类型且长度固定的数据项序列
- 数组是值类型

## 1.1 数组的定义

```go
package main

import (
	"fmt"
)

func main() {
    // 使用var关键字定义
	var a1 [4]int
	fmt.Println(a1)
    // ---> [0 0 0 0]

	var a2 = [4]int{}
	fmt.Println(a2)
    // ---> [0 0 0 0]

    // 使用{}传入值
	var a3 = [4]int{9, 5, 2, 7}
	fmt.Println(a3)
    // ---> [9 5 2 7]

    // 使用...，编译器会自动推断数组的长度
	a4 := [...]int{9, 5, 2, 7}
	fmt.Println(a4, len(a4), cap(a4))
    // ---> [9 5 2 7] 4 4

    // 使用：指明传入值的索引位置
	a5 := [...]string{1:"Luffy", 4:"Hancock"}
	fmt.Println(a5)
    // ---> [ Luffy   Hancock]

	a5[0] = "Nami"
	fmt.Println(a5)
    // ---> [Nami Luffy   Hancock]
}
```

## 1.2 数组的访问

数组通过下标索引来访问，语法与 python 类似。

```go
package main

import (
	"fmt"
)

func main() {
	a5 := [...]int{9, 5, 2, 7}
	fmt.Printf("%p, %v\n", &a5, a5)
    // ---> 0xc0000ae000, [9 5 2 7]

	a5[0] = 100
	fmt.Printf("%p, %v\n", &a5, a5)
    // ---> 0xc0000ae000, [100 5 2 7]
}
```

## 1.3 数组的遍历

```go
package main

import (
	"fmt"
)

func main() {
	a6 := [...]string {"Luffy", "Zoro", "Hancock", "Nami", "Robin"}

	for i:=0; i<len(a6); i++ {
		fmt.Println(a6[i])
	}
    // ---> Luffy
	// ---> Zoro
	// ---> Hancock
	// ---> Nami
	// ---> Robin

	// 使用range
	for i,v := range a6 {
		fmt.Println(i, v)
	}
    // ---> 0 Luffy
	// ---> 1 Zoro
	// ---> 2 Hancock
	// ---> 3 Nami
	// ---> 4 Robin
}
```

## 1.4 多维数组

```go
package main

import (
	"fmt"
)

func main() {
	a7 := [3][4]int{{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}}
	fmt.Println(a7)
	// ---> [[1 2 3 4] [5 6 7 8] [9 10 11 12]]

	a8 := [2][3][4]int{
		{{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}},
		{{13, 14, 15, 16}, {17, 18, 19, 20}, {21, 22, 23, 24}},
	}
	fmt.Println(a8)
    // ---> [[[1 2 3 4] [5 6 7 8] [9 10 11 12]]
    // ---> [[13 14 15 16] [17 18 19 20] [21 22 23 24]]]
}
```

# 2 切片（slice）

- 切片是数组的抽象，本身不存储数据，而是存储底层数组的地址
- 切片是引用类型
- 切片是可变的

## 2.1 切片的定义

```go
package main

import (
	"fmt"
)

func main() {

	var s1 []int
    fmt.Printf("%T, %v\n", s1, s1)
    fmt.Println(len(s1), cap(s1)) // 打印长度和容量
	// ---> []int, []
	// ---> 0 0

    var s2 = []int{1, 2, 3, 4, 5}
    fmt.Printf("%T, %v\n", s2, s2)
    fmt.Println(len(s2), cap(s2))
    // ---> []int, [1 2 3 4 5]
	// ---> 5 5

    s3 := make([]int, 3, 5)
    fmt.Println(s3, len(s3), cap(s3))
    // ---> [0 0 0] 3 5
}
```

## 2.2 切片的访问

- 当向切片中添加数据时，若添加的数量总和超过切片的容量，切片会自动扩容，且容量成倍增加
- 切片扩容本质是指向了一个新的数组，原来的数组被系统自动回收

```go
package main

import (
	"fmt"
)

func main() {

	s1 := make([]int, 0, 4)
	fmt.Printf("%v, %p\n", s1, s1)
	fmt.Printf("length:%d, capacity:%d\n", len(s1), cap(s1))
    // ---> [], 0xc0000b2000
	// ---> length:0, capacity:4

	s1 = append(s1, 1, 2)
	fmt.Printf("%v, %p\n", s1, s1)
	fmt.Printf("length:%d, capacity:%d\n", len(s1), cap(s1))
	// ---> [1 2], 0xc0000b2000
    // ---> length:2, capacity:4
    // 添加元素未超过容量，内存地址不变，依然是原来的数组

	s1 = append(s1, 3, 4, 5)
	fmt.Printf("%v, %p\n", s1, s1)
	fmt.Printf("length:%d, capacity:%d\n", len(s1), cap(s1))
    // ---> [1 2 3 4 5], 0xc0000b6000
    // ---> length:5, capacity:8
    // 添加元素超过容量，切片指向新的数组，容量成倍增加

}
```

从数组创建切片类似 python 的切片操作，使用 `[a:b]`，前闭后开。

```go
package main

import (
	"fmt"
)

func main() {

	s1 := [8]int{1, 2, 3, 4, 5, 6, 7, 8}
	s2 := s1[:]
	fmt.Printf("%v, %p， %p\n", s2, &s1, s2)
	fmt.Println(len(s2), cap(s2))
    // ---> [1 2 3 4 5 6 7 8], 0xc0000ae000， 0xc0000ae000
	// ---> 8 8

	s3 := s1[0:3]
	fmt.Printf("%v, %p, %p\n", s3, &s1, s3)
	fmt.Println(len(s3), cap(s3))
	// ---> [1 2 3], 0xc0000ae000, 0xc0000ae000
	// ---> 3 8

	s4 := s1[3:6]
	fmt.Printf("%v, %p, %p\n", s4, &s1, s4)
	fmt.Println(len(s4), cap(s4))
    // ---> [4 5 6], 0xc0000ae000, 0xc0000ae018
	// ---> 3 5
    // 切片的长度即为截取的数组的长度，容量是从截取起始位置到数组末尾的长度
    // 数组的地址是数组中首个元素的地址，s4由于截取的起始索引为3，所以s4的地址与s1不同
}
```

切片本质上是一种特殊的指针，存储的是底层数组的地址。

```go
package main

import (
	"fmt"
)

func main() {

	s1 := [8]int{1, 2, 3, 4, 5, 6, 7, 8}
	s2 := s1[:6]
	s1[0] = 100
	fmt.Printf("%p, %p\n", &s1, s2)
	fmt.Println(s1, s2)
	// ---> 0xc00001e140, 0xc00001e140
	// ---> [100 2 3 4 5 6 7 8] [100 2 3 4 5 6]
    // 切片指向底层数组，底层数组改变，切片相应改变

	s2[3] = 50
	fmt.Printf("%p, %p\n", &s1, s2)
	fmt.Println(s1, s2)
    // ---> 0xc00001e140, 0xc00001e140
	// ---> [100 2 3 50 5 6 7 8] [100 2 3 50 5 6]
    // 切片改变，也会导致底层数组改变

	s2 = append(s2, 25)
	fmt.Printf("%p, %p\n", &s1, s2)
	fmt.Println(s1, s2)
    // ---> 0xc00001e140, 0xc00001e140
    // ---> [100 2 3 50 5 6 25 8] [100 2 3 50 5 6 25]

}

```

切片是引用类型。

```go
package main

import (
	"fmt"
)

func main() {

	s1 := []int{1, 2, 3, 4}
	s2 := s1
	fmt.Println(s1, s2)
	fmt.Printf("s1底层数组的地址:%p, s1的地址:%p\n", &s1, s1)
	fmt.Printf("s2底层数组的地址:%p, s2的地址:%p\n", &s2, s2)
    // ---> [1 2 3 4] [1 2 3 4]
	// ---> s1底层数组的地址:0xc00000c060, s1的地址:0xc0000144a0
	// ---> s2底层数组的地址:0xc00000c080, s2的地址:0xc0000144a0
    // s1，s2指向同一个底层数组

	s1[0] = 100
	fmt.Println(s1, s2)
	fmt.Printf("s1底层数组的地址:%p, s1的地址:%p\n", &s1, s1)
	fmt.Printf("s2底层数组的地址:%p, s2的地址:%p\n", &s2, s2)
    // ---> [100 2 3 4] [100 2 3 4]
	// ---> s1底层数组的地址:0xc00000c060, s1的地址:0xc0000144a0
	// ---> s2底层数组的地址:0xc00000c080, s2的地址:0xc0000144a0
    // 改变s1，s2同时也会改变

	s2[3] = 50
	fmt.Println(s1, s2)
	fmt.Printf("s1底层数组的地址:%p, s1的地址:%p\n", &s1, s1)
	fmt.Printf("s2底层数组的地址:%p, s2的地址:%p\n", &s2, s2)
    // ---> [100 2 3 50] [100 2 3 50]
	// ---> s1底层数组的地址:0xc00000c060, s1的地址:0xc0000144a0
	// ---> s2底层数组的地址:0xc00000c080, s2的地址:0xc0000144a0
	// 改变s2，s1同时也会改变
}
```

# 3 map

- map 类似于 python 中的字典，也是以键值对的方式存储数据
- map 是引用类型
- map 是可变的

## 3.1 map 的定义

```go
package main

import (
    "fmt"
)

func main() {
    var m1 map[string]int
	fmt.Printf("%T, %v\n", m1, m1)
    // ---> map[string]int, map[]
	// 这种定义方式，m1并未初始化，是nil类型，不能直接赋值
	m1["Jay"] = 1
    // ---> panic: assignment to entry in nil map

	var m2 = map[string]int{"Jay": 1, "Edison": 2, "Luffy": 3}
	fmt.Printf("%T, %v\n", m2, m2)
    // ---> map[string]int, map[Edison:2 Jay:1 Luffy:3]

	m3 := map[string]int{"Jay": 1, "Edison": 2, "Luffy": 3}
	fmt.Printf("%T, %v\n", m3, m3)
    // ---> map[string]int, map[Edison:2 Jay:1 Luffy:3]

    // 使用make函数
	m4 := make(map[string]int)
	fmt.Printf("%T, %v\n", m4, m4)
    // ---> map[string]int, map[]
}
```

## 3.2 map 的访问

map 使用 key 进行访问与赋值

```go
package main

import (
	"fmt"
)

func main() {
    m5 := make(map[int]string)
	m5[1] = "Jay"
	m5[2] = "Edison"
	m5[3] = "Luffy"
	m5[4] = "Perl"
	m5[5] = "Mads"
	m5[6] = "Joker"
	fmt.Println(m5)
    // map[1:Jay 2:Edison 3:Luffy 4:Perl 5:Mads 6:Joker]

	fmt.Println(m5[3])
    // Luffy
}
```

## 3.3 map 的遍历

```go
package main

import (
	"fmt"
)

func main() {
    m6 := map[string]string{"name":"Luffy", "sex":"male", "age":"18", "address":"East blue"}
	for k,v := range m6 {
		fmt.Printf("%s : %s\n", k, v)
	}
}
// ---> name : Luffy
// ---> sex : male
// ---> age : 18
// ---> address : East blue
```

# 4 指针（pointer)

指针是一种特殊的变量，用于保存另一变量的内存地址。

## 4.1 指针的定义

```go
package main

import (
	"fmt"
)

func main() {
	var p1 *[4]int
	fmt.Println(p1)
    // ---> <nil> // <nil>表示空指针
	a := [4]int{1, 2, 3, 4}
	p1 = &a // &为取地址符
	fmt.Println(p1)
    // ---> &[1 2 3 4]
	fmt.Printf("%p, %p\n", p1, &p1) // 第一个占位符表示p1保存的地址，第二个占位符表示p1自身的地址
    // ---> 0xc0000b0000, 0xc0000a8018
}
```

## 4.2 指针的访问

go 语言中使用 \* 来取指针所保存的内存地址指向的变量值。

```go
package main

import (
	"fmt"
)

func main() {
	var p2 *[4]string
	a2 := [4]string {"Luffy", "Hancock", "Zoro", "Nami"}

	p2 = &a2
	fmt.Println(*p2)
    // ---> [Luffy Hancock Zoro Nami]

	(*p2)[0] = "Robin"
	fmt.Println(p2)
    // ---> &[Robin Hancock Zoro Nami]
	fmt.Println(a2)
    // ---> [Robin Hancock Zoro Nami]

	p2[2] = "Shanks" // 简化写法
	fmt.Println(p2)
    // ---> &[Robin Hancock Shanks Nami]
	fmt.Println(a2)
    // ---> [Robin Hancock Shanks Nami]

}
```

## 4.3 指针的指针

指针的指针，顾名思义，该指针中保存的是另一个指针的地址。

```go
package main

import (
	"fmt"
)

func main() {
	var ptr *[4]int
	var pptr **[4]int

	a := [4]int{1, 2, 3, 4}
	ptr = &a
	pptr = &ptr

	fmt.Println(a)
    // ---> [1 2 3 4]
	fmt.Println(ptr, *ptr)
    // ---> &[1 2 3 4] [1 2 3 4]
	fmt.Println(pptr, *pptr)
    // ---> 0xc0000a8018 &[1 2 3 4]
}
```

# 5 函数

- 函数是一种特殊的指针变量
- 函数名指向函数体的内存地址
- 函数名加 `()` 调用函数，执行函数体内的全部代码，并通过 `return` 语句将执行结果返回给函数调用处

## 5.1 函数的定义

```go
func funcName(p1 type, p2 type)(v1 type, v2 type) {
    // 函数体
    return v1, v2
}

// eg:
func add(num1, num2 int)int {
    return num1+num2
}
```

```go
package main

import "fmt"

func main() {
	fmt.Printf("%T, %p\n", print, print)
    // ---> func(), 0x48eb50 // 函数体的地址

	var x func()
	x = print // 将print的值（函数体的地址）赋值给x
	x()
    // ---> Nami is alse good!
}

func print() {
	fmt.Println("Nami is alse good!")
}
```

## 5.2 函数的参数

### 5.2.1 可变参数

- 可变参数本质上是一个切片
- 在参数列表中，可变参数应放在最后
- 可变参数至多只能有一个

```go
package main

import "fmt"

func main() {
	add1()
    // ---> []int
    // 可变参数实质上是一个slice

	s := []int{1, 2, 3, 4, 5, 6}
	x := add2(s...) // 使用...提取slice中的元素
	fmt.Println(x)
    // ---> 21
}

func add1(num ...int) {
	fmt.Printf("%T\n", num)
}

func add2(num ...int) int {
	sum := 0
	for _, v := range num {
		sum = sum + v
	}

	return sum
}
```

### 5.2.2 参数传递

**值传递**，值传递传递的是参数的副本。值类型的数据默认都是值传递：基本数据类型、array、struct。

```go
package main

import "fmt"

func main() {
	arr := [4]int{1, 2, 3, 4}
	fmt.Printf("%p, %v\n", &arr, arr)
    // ---> 0xc0000ae000, [1 2 3 4]

	change(arr)
    // ---> 0xc0000ae060
	// ---> [10000 2 3 4]

    fmt.Println(arr)
    // ---> [1 2 3 4]
}

func change(a [4]int) {
	fmt.Printf("%p\n", &a)
	a[0] = 10000
	fmt.Println(a)
}
```

**引用传递**，引用传递传递的是参数的地址。引用类型的数据默认都是引用传递：slice、map、chan。

```go
package main

import "fmt"

func main() {
	slice := []int{1, 2, 3, 4}
	fmt.Println(slice)
	// ---> [1 2 3 4]

	change(slice)
    // ---> [10000 2 3 4]

	fmt.Println(slice)
    // ---> [10000 2 3 4]
}

func change(s []int) {
	s[0] = 10000
	fmt.Println(s)
}
```

## 5.3 递归函数

```go
func fibonacci(n int) int {
	if n == 1 || n == 2 {
		return 1
	}
	return fibonacci(n-1) + fibonacci(n-2)
}
```

## 5.4 defer 语句

`defer` 语句可以用来延迟一个函数或者方法的执行。当存在多个延迟调用时，它们被添加到一个堆栈中，遵循后进先出的原则执行。

```go
package main

import "fmt"

func main() {
	defer print()
	defer print2()
	fmt.Println("Hancock is good!")
    // ---> Hancock is good!
    // ---> Robin is good! // LIFO
    // ---> Nami is also good!
}

func print() {
	fmt.Println("Nami is also good!")
}

func print2() {
	fmt.Println("Robin is good!")
}
```

## 5.5 匿名函数

- 匿名函数可以作为另一个函数的参数，也叫回调函数
- 匿名函数可以作为另一个函数的返回值，也叫闭包结构

```go
package main

import "fmt"

func main() {
	func () {
		fmt.Println("Hancock!")
	}()
    // ---> Hancock!

	fun1 := func () {
		fmt.Println("Nami!")
	}
	fun1()
    // ---> Nami!

	// 带参数与返回值的匿名函数
	res := func (a, b int) int {
		return a+b
	}(1, 2)
	fmt.Println(res)
    // ---> 3
}
```

作为一个函数参数的函数就叫做回调函数。

```go
package main

import "fmt"

func main() {
	res := opr(1, 2, add)
	fmt.Println(res)
    // ---> 3
}

func add(a, b int) int {
	return a + b
}

func opr(a, b int, fun func(int,int)int) int {
	return fun(a, b)
}
```

使用匿名函数作为回调函数。

```go
package main

import "fmt"

func main() {
	add := func(a, b int) int {
		return a + b
	}
	res := opr(1, 2, add)
	fmt.Println(res)
    // ---> 3

	res2 := opr(1, 2, func(a, b int) int {
		return a + b
	})
	fmt.Println(res2)
    // ---> 3
}

func opr(a, b int, fun func(int, int) int) int {
	return fun(a, b)
}
```

一个外层函数有内层函数，内层函数会操作外层函数的局部变量（外层函数的参数，或者外层函数定义的局部变量），并且该外层函数的返回值就是这个内层函数，那么这个内层函数和外层函数的局部变量就统称为闭包结构。

闭包中局部变量的生命周期会发生改变。正常的局部变量会随着外层函数的调用而创建，随着外层函数的结束而销毁。但是闭包结构中外层函数的局部变量不会随着外层函数的结束而销毁，因为内层函数还要继续使用。

```go
package main

import (
	"fmt"
)

func main() {
	fmt.Printf("%p\n", increment)
    // ---> 0x48f0f0 // 函数名所指向的函数体的地址
	res1 := increment()
	fmt.Printf("%p, %p\n", res1, &res1)
    // ---> 0x48f190, 0xc00000e030 // 内层函数体的地址， res1变量的地址
	fmt.Println(res1())
    // ---> 1
	fmt.Println(res1())
    // ---> 2
	fmt.Println(res1())
    // ---> 3

	res2 := increment()
	fmt.Println(res2())
    // ---> 1
	fmt.Println(res2())
    // ---> 2

	fmt.Println(res1())
    // ---> 4

	var fun func() func() int
	fun = increment
	fmt.Printf("%p\n", fun)
    // ---> 0x48f0f0
	fmt.Printf("%p\n", &fun)
    // ---> 0xc00000e038

	fun2 := increment
	fmt.Printf("%p\n", fun2)
    // ---> 0x48f0f0
	fmt.Printf("%p\n", &fun2)
    // ---> 0xc00000e040

}

func increment() func() int {
	i := 0 //这个外层函数的局部变量，是内层函数的全局变量
	return func() int {
		i++
		return i
	}
}
```

# 6 结构体

- 结构体是一系列相同类型或不同类型的数据构成的集合
- 结构体是由一个个成员变量构成的，这些成员变量也叫做结构体的字段
- 结构体是可变的
- 结构体是值类型

## 6.1 结构体的定义

```go
// 结构体使用type和struct关键字来进行声明
type Person struct {
    name string
    sex string
    age int
    address string
}
```

## 6.2 结构体的初始化与访问

```go
// 结构体使用.操作符来进行访问
// 使用var关键字初始化
var P1 Person
p1.name = "Jay"
p1.sex = "male"
p1.age = "41"
p1.address = "Taibei"

// 类似简短声明
p2 := Person{}
p2.name = "Zoro"
p2.sex = "male"
p2.age = "20"
p2.address = "East Blue"

// 按照field:value的方式提供初始化的值
p3 := Person{
    name ： "Luffy",
    sex ： "male",
    age ： 18,
    address : "East Blue",
}

// 按照顺序提供初始化的值
p4 := Person{"Hancock", "female", 29, "East Blue"}
```

```go
package main

import (
	"fmt"
)

func main() {
	p1 := Person{
		name:    "Hancock",
		sex:     "female",
		age:     29,
		address: "East Blue",
	}

	fmt.Println(p1)
    // ---> {Hancock female 29 East Blue}
    // 结构体使用.操作符来进行访问
	p1.age = 31
	fmt.Println(p1)
    // ---> {Hancock female 31 East Blue}
}

type Person struct {
	name    string
	sex     string
	age     int
	address string
}
```

## 6.3 结构体指针

```go
package main

import(
	"fmt"
)

func main() {
	p1 := Person {
		name : "Hancock",
		sex : "female",
		age : 29,
		address : "East Blue",
	}

	var pp1 *Person
	pp1 = &p1
	fmt.Printf("%p, %T\n", pp1, pp1)
    // ---> 0xc0000240c0, *main.Person
	fmt.Println(*pp1)
    // ---> {Hancock female 29 East Blue}

	// 使用指针修改数据
	(*pp1).name = "Nami"
	fmt.Println(pp1, p1)
    // ---> &{Nami female 29 East Blue} {Nami female 29 East Blue}
	// 简写
	pp1.name = "Robin"
	fmt.Println(pp1, p1)
    // ---> &{Robin female 29 East Blue} {Robin female 29 East Blue}

    // 使用new函数创建指针
    // new函数指向了新开辟的内存空间，里面存储的是0值
    pp2 := new(Person)
	fmt.Printf("%T\n", pp2)
    // ---> *main.Person
	fmt.Println(pp2)
    // ---> &{  0 }

	pp2.name = "Luffy"
	pp2.sex = "male"
	pp2.age = 18
	pp2.address = "East Blue"
	fmt.Println(pp2)
    // ---> &{Luffy male 18 East Blue}
}

type Person struct {
	name string
	sex string
	age int
	address string
}
```

## 6.4 匿名结构体与匿名字段

```go
package main

import(
	"fmt"
)

func main() {
    // 匿名结构体
	p1 := struct {
		name string
		sex string
		age int
		address string
	} {
		name : "Hancock",
		sex : "female",
		age : 29,
		address : "East Blue",
	}
	fmt.Println(p1)
    // ---> {Hancock female 29 East Blue}

    // 结构体使用匿名字段时，默认使用字段类型作为field，因此字段类型不能重复
	p2 := Person {"Hancock", 29}
	fmt.Println(p2)
	// ---> {Hancock 29}
	fmt.Println(p2.string)
    // ---> Hancock

    // 同时使用匿名结构体和匿名字段
	p3 := struct {
		string
		int
	} {
		"Hancock",
		29,
	}
	fmt.Println(p3)
    // ---> {Hancock 29}
	fmt.Println(p3.string)
    // ---> Hancock
}

type Person struct {
	string
	int
}
```

## 6.5 结构体嵌套

```go
package main

import(
	"fmt"
)

func main() {
	p1 := Person {
		name : Name {
			firstName : "Hancock",
			lastName : "Boa",
		},
		sex : "female",
		age : 29,
		address : "East Blue",
	}

	fmt.Printf("姓：%s，名：%s，性别：%s，年龄：%d，地址：%s\n", p1.name.lastName, p1.name.firstName, p1.sex, p1.age, p1.address)
    // ---> 姓：Boa，名：Hancock，性别：female，年龄：29，地址：East Blue
}

type Name struct {
	firstName string
	lastName string
}

type Person struct {
	name Name
	sex string
	age int
	address string
}
```

由于结构体是值类型，因此在嵌套时也可以选择嵌套结构体指针，可以保持数据的一致性，同时节省内存。

```go
package main

import(
	"fmt"
)

func main() {
	n1 := Name {
		firstName : "Hancock",
		lastName : "Boa",
	}

	p1 := Person {
		name : &n1,
		sex : "female",
		age : 29,
		address : "East Blue",
	}

	fmt.Printf("姓：%s，名：%s，性别：%s，年龄：%d，地址：%s\n", p1.name.lastName, p1.name.firstName, p1.sex, p1.age, p1.address)
    // ---> 姓：Boa，名：Hancock，性别：female，年龄：29，地址：East Blue

	p1.name.lastName = "Monkey D"
	fmt.Println(n1)
    // 修改p1，n1同时改变，数据保持一致
    // ---> {Hancock Monkey D}
}

type Name struct {
	firstName string
	lastName string
}

type Person struct {
	name *Name // 传入指针
	sex string
	age int
	address string
}
```

假如说结构体中同时包含匿名字段与非匿名字段，特别的，当匿名字段为指针时，在实例化结构体时要给匿名字段加上字段名，且该字段名就是指针对应的类型，否则会报错 `mixture of field:value and value initializers` 。

```go
package main

import (
	"fmt"
)

func main() {
	hancock := Person{
		name:   "Hancock",
		age:    29,
		gender: "female",
	}
	var han *Person = &hancock
	hanworker := Worker{
		Person: han, // 要用指针对应的类型作为字段名
		skill:  "bj",
		salary: 200,
	}

	fmt.Println(hanworker)
}

type Person struct {
	name   string
	age    int
	gender string
}

type Worker struct {
	*Person
	skill  string
	salary int
}
```