/**
 * @file /include/ecl/ipc/shared_memory_pos.hpp
 *
 * @brief The posix implementation for shared memory.
 *
 * Requires _POSIX_SHARED_MEMORY_OBJECTS
 *
 * @date August 2009
 **/
/*****************************************************************************
** Ifdefs
*****************************************************************************/

#ifndef ECL_IPC_SHARED_MEMORY_RT_HPP_
#define ECL_IPC_SHARED_MEMORY_RT_HPP_

/*****************************************************************************
** Platform Check
*****************************************************************************/

#include <ecl/config.hpp>
#if defined(ECL_IS_POSIX)
#include <unistd.h>
#include <bits/posix_opt.h>
#ifdef _POSIX_SHARED_MEMORY_OBJECTS
#if _POSIX_SHARED_MEMORY_OBJECTS > 0

/*****************************************************************************
** Ecl Functionality Defines
*****************************************************************************/

#ifndef ECL_HAS_POSIX_SHARED_MEMORY
  #define ECL_HAS_POSIX_SHARED_MEMORY
#endif
#ifndef ECL_HAS_SHARED_MEMORY
  #define ECL_HAS_SHARED_MEMORY
#endif

/*****************************************************************************
** Includes
*****************************************************************************/

#include <sstream>
#include <string>
#include <sys/mman.h>        /* For shm_open() */
#include <fcntl.h>           /* For O_* constants */
#include <ecl/exceptions/macros.hpp>
#include <ecl/exceptions/standard_exception.hpp>
#include <ecl/config/macros.hpp>

/*****************************************************************************
** Namespaces
*****************************************************************************/

namespace ecl {

/*****************************************************************************
** Exception Handling
*****************************************************************************/

namespace ipc {

#ifdef ECL_HAS_EXCEPTIONS

/**
 * @brief Posix exception handler for opening shared memory.
 *
 * This function generates a custom StandardException response
 * for posix error numbers generated by open requests within
 * the SharedMemory class.
 * @param loc : use with the LOC macro, identifies the line and file of the code.
 */
// Have to be public since its called from a template (inline) function.
ECL_PUBLIC ecl::StandardException openSharedSectionException(const char* loc);
/**
 * @brief Posix exception handler for shared memory mappings.
 *
 * This function generates a custom StandardException response
 * for posix error numbers generated by memory mapping calls within
 * the SharedMemory class.
 * @param loc : use with the LOC macro, identifies the line and file of the code.
 */
ECL_PUBLIC ecl::StandardException memoryMapException(const char* loc);


#endif /* ECL_HAS_EXCEPTIONS */

/**
 * @brief Common shared memory functions wrapping the underlying rt calls.
 *
 * This is a bit of magic to make sure that the rt calls are always
 * called in the implementation (cpp files). This way the library doesn't
 * get underlinked for rt.
 */
class ECL_PUBLIC SharedMemoryBase {
public:
	/**
	 * @brief Unlink the memory.
	 *
	 * Mapped processes may still use, but no new objects can connect to it.
	 **/
	void unlink();

protected:
	SharedMemoryBase(const std::string &name_id) :
		name(name_id),
		shared_memory_manager(false)
	{};
	/**
	 * @brief Open and configure the shared memory.
	 *
	 * Does a fair bit of automatic configuration here.
	 *
	 * @return int : -1 is a fail, success is anything else.
	 */
	int open();

	std::string name;
	bool shared_memory_manager;
};

} // namespace ipc

/*****************************************************************************
** Shared Memory
*****************************************************************************/
/**
 * @brief Templatised interface for shared memory.
 *
 * Templatises the interface for shared memory by representing the
 * storage area by the templatised data type.
 *
 * The templatised data type must be a type that has a fixed size as it
 * is its own size that determines the size of the storage area. Be
 * careful about using stl containers (strings, vectors etc). Even if
 * you fix their capacity, I'm not yet sure how they will behave.
 **/
template <typename Storage>
class ECL_PUBLIC SharedMemory : public ipc::SharedMemoryBase
{
public:
	/*********************
	** C&D's
	**********************/
	SharedMemory(const std::string& string_id) ecl_throw_decl(StandardException);
	virtual ~SharedMemory();

	Storage* data() { return storage; }         /**< Data storage accessor. **/

private:
	SharedMemory() {} /**< @brief Default constructor - use is forbidden. **/
	const int shared_memory_size;
	Storage *storage;
};

/*****************************************************************************
** Implementation
*****************************************************************************/

/**
 * @brief RIAA style shared memory initialiser.
 *
 * Configures the shared memory with the given pathname and if it
 * is created (not already existing), it uses a default storage structure (Storage())
 * to initialise shared memory region.
 *
 * @param string_id : unique string identifier for the shared memory (no slashes)
 *
 * @exception StandardException : throws if the shared memory could not be initialised.
 **/
template <typename Storage>
SharedMemory<Storage>::SharedMemory(const std::string& string_id ) ecl_throw_decl(StandardException)  :
	ipc::SharedMemoryBase(std::string("/")+string_id),
	shared_memory_size(sizeof(Storage)),
	storage(NULL)
{
	int shm_descriptor = open();
    if ( shm_descriptor == -1) {
        ecl_throw( ipc::openSharedSectionException(LOC) );
    }
    /*********************
     * Mapping
     *********************/
    /*
     * Map the shared memory into your process's address space.
     *
     * Address: 0 lets posix choose the address.
     * Memory Protections: PROT_READ,WRITE,EXEC,NONE. Tells the MMU what to do. Match with the shm_open parameters.
     *                     PROT_EXEC only useful if you want to run a shared library there.
     * Mapping Flags: Always choose MAP_SHARED for shared memory! Other options almost irrelevant.
     * Descriptor : shm_send_descriptor from above.
     * OFFSET : we should never really want to offset a chunk of memory. Just point it at the start (0).
     *
     * mmap(address,sharedMemSize,memprotections,mappingflags,descriptor,offset);
     */
    void * shm_address;
    if ( (shm_address = mmap(0,shared_memory_size,PROT_READ|PROT_WRITE,MAP_SHARED,shm_descriptor,(long) 0)) == MAP_FAILED )
    {
        shared_memory_manager = false;
        close(shm_descriptor);
        unlink();
        ecl_throw( ipc::memoryMapException(LOC) );
    }
    /*
     * When first created, the shared memory has 0 size. You need to inflate it before
     * you can use it. The second argument, the length is measured in bytes.
     */
    if ( ftruncate(shm_descriptor,shared_memory_size) < 0 )
    {
        shared_memory_manager = false;
        close(shm_descriptor);
        unlink();
        ecl_throw(StandardException(LOC,OpenError,"Shared memory created, but inflation to the desired size failed."));
    }

    /*********************
    ** Close
    **********************/
    /*
     * This does not unmap the memory allocated to the block. It just closes the file
     * descriptor. Should do it early for tidiness if for no other reason.
     */
    close(shm_descriptor);

    storage = (Storage*) shm_address;

    // If just allocated, initialise the shared memory structure.
    if ( shared_memory_manager ) {
        *storage = Storage();
    }
}
/**
 * Default destructor. Closes the file descriptor and unlinks the name so that no-one else
 * can open into the shared memory. Once all processes finish with it, the shared memory
 * disintegrates.
 **/
template <typename Storage>
SharedMemory<Storage>::~SharedMemory()
{
    /* Might be worth putting a check on this later (i.e. < 0 is an error). */
    munmap( (void*) storage,shared_memory_size);
//    munmap(shm_address,shared_memory_size);

    if ( shared_memory_manager ) {
        unlink();
    }
}

}; // namespace ecl


#endif /* _POSIX_SHARED_MEMORY_OBJECTS > 0 */
#endif /* _POSIX_SHARED_MEMORY_OBJECTS */
#endif /* ECL_IS_POSIX */

#endif /* ECL_IPC_SHARED_MEMORY_RT_HPP_ */
