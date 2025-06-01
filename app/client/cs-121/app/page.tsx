"use client"

import {z} from "zod"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form"

import {
  HoverCard,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import { Input } from "@/components/ui/input"
import { useState } from "react"

const formSchema = z.object({
  username: z.string().min(2).max(50),
})



export default function Home() {

  const [urls, setUrls] = useState([])
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
    },
  })
 
  // 2. Define a submit handler.
  async function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.

    try {

      const response = await fetch("http://127.0.0.1:5000/search",  
      {method: 'POST', headers: {'Content-Type': 'application/json',}, 
      body: JSON.stringify(values)})

      if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
      }

    console.log(JSON.stringify(values))
    console.log(values)
    const json = await response.json();
    console.log("Testing the value json: ", json);
    setUrls(json)
    } catch (error){
        console.error('Error:', error)
    }
  }

return (
  <div className="bg-black flex justify-center items-center min-h-screen flex-col">

    {/* <h1 className="text-white text-3xl">Enter query</h1> */}
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 flex items-center">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Input placeholder="shadcn" {...field} className="mt-8 text-white"/>
              </FormControl>
              {/* <FormDescription>
                This is your public display name.
              </FormDescription> */}
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>

    <div className="flex flex-col space-y-3 justify-center items-center">
          {urls.map((url, index) =>

              <a href={url} className="text-white hover:text-blue-500 px-5 py-2 rounded-3xl" key={index}>{url}</a>

          )}
    </div>

    </div>
  )
}
