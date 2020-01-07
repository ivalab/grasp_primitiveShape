/*
 * Copyright (c) 2014-2016 Spotify AB
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

#pragma once

#include <cstdlib>

#if defined(_MSC_VER)
  #define json_force_inline __forceinline
  #define json_never_inline __declspec(noinline)
  #define json_noreturn __declspec(noreturn)
  #define json_likely(expr) (expr)
  #define json_unlikely(expr) (expr)
  #define json_unreachable() std::abort()
#elif defined(__GNUC__)
  #define json_force_inline __attribute__((always_inline)) inline
  #define json_never_inline __attribute__((noinline))
  #define json_noreturn __attribute__((noreturn))
  #define json_likely(expr) __builtin_expect(!!(expr), 1)
  #define json_unlikely(expr) __builtin_expect(!!(expr), 0)
  #define json_unreachable() __builtin_unreachable()
#else
  #define json_force_inline inline
  #define json_never_inline
  #define json_noreturn
  #define json_likely(expr) (expr)
  #define json_unlikely(expr) (expr)
  #define json_unreachable() std::abort()
#endif  // _MSC_VER

#ifdef max
  #undef max
#endif  // max

#ifdef min
  #undef min
#endif  // min

#define json_size_t_max static_cast<size_t>(-1)

// http://graphics.stanford.edu/~seander/bithacks.html
#define json_haszero_1(v) (!(v))
#define json_haszero_2(v) uint16_t(((v) - 0x0101U) & ~(v) & 0x8080U)
#define json_haszero_4(v) uint32_t(((v) - 0x01010101UL) & ~(v) & 0x80808080UL)
#define json_haszero_8(v) uint64_t(((v) - 0x0101010101010101ULL) & ~(v) & 0x8080808080808080ULL)
#define json_haschar_1(v, c) (v == c)
#define json_haschar_2(v, c) uint16_t(json_haszero_2((v) ^ (~0U/255 * (c))))
#define json_haschar_4(v, c) uint32_t(json_haszero_4((v) ^ (~0UL/255 * (c))))
#define json_haschar_8(v, c) uint64_t(json_haszero_8((v) ^ (~0ULL/255 * (c))))
#define json_unaligned_1(p) false
#define json_unaligned_2(p)  (reinterpret_cast<intptr_t>(p) & 0x1)
#define json_unaligned_4(p)  (reinterpret_cast<intptr_t>(p) & 0x3)
#define json_unaligned_8(p)  (reinterpret_cast<intptr_t>(p) & 0x7)
#define json_unaligned_16(p) (reinterpret_cast<intptr_t>(p) & 0xF)

// http://sourceforge.net/p/predef/wiki/Architectures/
// http://nadeausoftware.com/articles/2012/02/c_c_tip_how_detect_processor_type_using_compiler_predefined_macros

#if defined(__i386__) || defined(__i386) || \
    defined(_M_IX86) || defined(_X86_)
  #define json_arch_x86_32
#endif

#if defined(__x86_64__) || defined(__x86_64) || \
    defined(__amd64__) || defined(__amd64) || \
    defined(_M_X64) || defined(_M_AMD64)
  #define json_arch_x86_64
#endif

#if defined(json_arch_x86_32) || defined(json_arch_x86_64)
  #define json_arch_x86
#endif

#if defined(json_arch_x86) && defined(SPOTIFY_JSON_USE_SSE42)
  #define json_arch_x86_sse42
#endif
