'''
Copyright (c) 2022 Algorand Name Service DAO LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from pyteal import *
from . import constants

def ValidateRecord(name, timestamp):

    i = ScratchVar(TealType.uint64)

    is_valid_txn = Seq([

        Assert(Len(Bytes(name)) <= Int(64)),
        For(i.store(Int(0)), i.load() < Len(Bytes(name)), i.store(i.load() + Int(1))).Do(
            Assert(
                Or(
                    And(
                        GetByte(Bytes(name), i.load()) >= Int(constants.ASCII_LOWER_CASE_A),
                        GetByte(Bytes(name), i.load()) <= Int(constants.ASCII_LOWER_CASE_Z)
                    ),
                    And(
                        GetByte(Bytes(name), i.load()) >= Int(constants.ASCII_DIGIT_0),
                        GetByte(Bytes(name), i.load()) <= Int(constants.ASCII_DIGIT_9)
                    )
                )
            )
        ),
        
        Int(1)     
    ])

    subscribe = Seq([
        Assert(Int(timestamp) > Global.latest_timestamp()),
        Assert(is_valid_txn),
        Return(Int(1))
    ])

    revoke = Seq([
        Assert(Int(timestamp) < Global.latest_timestamp()),
        Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
        Assert(Gtxn[2].type_enum() == TxnType.AssetTransfer),
        Assert(Gtxn[3].type_enum() == TxnType.AssetConfig),
        Return(Int(1))
    ])

    optin = Seq([
        Assert(Txn.type_enum() == TxnType.AssetTransfer),
        Return(Int(1))
    ])

    program = Cond(
        [Arg(0) == Bytes("subscribe"), subscribe],
        [Arg(0) == Bytes("revoke"), revoke],
        [Arg(0) == Bytes("optin"), optin]
    )

    return program
