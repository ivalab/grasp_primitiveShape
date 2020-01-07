/*
 * Copyright (c) 2016 Spotify AB
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

#include <stdexcept>
#include <string>

#include <spotify/json/detail/macros.hpp>

namespace spotify {
namespace json {

/**
 * encode_exception objects are thrown when encoding fails, for example when
 * trying to encode a null smart pointer or a NaN floating point number.
 */
class encode_exception final : public std::runtime_error {
 public:
  template <typename string_type>
  explicit json_never_inline encode_exception(const string_type &what)
      : runtime_error(what) {}
};

}  // namespace json
}  // namespace spotify
